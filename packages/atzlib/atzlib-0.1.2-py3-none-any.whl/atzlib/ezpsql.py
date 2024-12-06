import logging
import os

from sqlalchemy import UniqueConstraint, Table, Column, String, MetaData, create_engine, text, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

import pandas as pd
from multiprocessing import Pool, cpu_count

from dotenv import load_dotenv
load_dotenv()

# 로그 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect_db():
    """데이터베이스 자동연결. config.yaml 정보 확인 후 연결 시도.

    Returns:
        engine: 연결된 데이터베이스 엔진

    Raises:
        FileNotFoundError: config.yaml 파일이 존재하지 않을 경우 발생.
        KeyError: config.yaml 파일에 필요한 데이터베이스 정보가 없을 경우 발생.
        SQLAlchemyError: 데이터베이스 연결 중 발생하는 SQLAlchemy 관련 오류 처리.
        Exception: 기타 예상치 못한 오류 처리.
    """
    try:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")

        engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        )
        return engine

    except KeyError as e:
        print(f"'{e}' 키가 없습니다.")
    except exc.SQLAlchemyError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")

def create_table_from_csv(df, table_name, primary_keys, foreign_keys=None):
    """
    pandas DataFrame에서 SQLAlchemy 테이블을 생성합니다.

    Args:
        df (pandas.DataFrame): 테이블을 생성할 DataFrame.
        table_name (str): 생성할 테이블 이름.
        primary_keys (list of str): 기본 키 컬럼들.
        foreign_keys (dict, optional): 컬럼 이름과 외래 키 참조를 매핑하는 딕셔너리.

    Returns:
        sqlalchemy.Table: 생성된 SQLAlchemy 테이블.
    """
    engine = connect_db()
    metadata = MetaData()
    
    columns = []

    for col_name in df.columns:
        column = Column(col_name, String, quote=True)
        columns.append(column)

    unique_constraint = UniqueConstraint(*primary_keys, name=f"{table_name}_uc")
    columns.append(unique_constraint)

    table = Table(table_name, metadata, *columns, extend_existing=True)
    metadata.create_all(engine)
    
    return table


def clear_table(table_name):
    """데이터베이스에서 지정된 테이블을 삭제합니다.

    Args:
        table_name (str): 삭제할 테이블 이름.

    Notes:
        테이블이 존재하지 않을 경우에도 오류 없이 진행되며, 테이블과 연관된 모든 종속 객체도 함께 삭제됩니다.
        `metadata.clear()`는 SQLAlchemy에서 메타데이터 캐시를 비우는 역할을 합니다.
    """
    engine = connect_db()
    metadata = MetaData()
    
    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
    metadata.clear()


def detect_and_remove_duplicates(df, primary_keys):
    """주어진 데이터프레임에서 기본 키(primary keys)를 기준으로 중복된 행을 감지하고 제거합니다.

    Args:
        df (pd.DataFrame): 중복을 감지할 데이터프레임.
        primary_keys (list): 중복을 확인할 기본 키 열의 리스트.

    Returns:
        tuple: 두 개의 데이터프레임을 반환합니다.
            - duplicates (pd.DataFrame): 중복된 모든 행이 포함된 데이터프레임.
            - unique_df (pd.DataFrame): 중복이 제거된 데이터프레임.

    Notes:
        `keep=False`를 사용하여 중복된 모든 행을 `duplicates` 데이터프레임에 포함시킵니다.
        `unique_df`는 중복된 행 중 첫 번째 행만 남기고 제거합니다.
    """
    duplicates = df[df.duplicated(subset=primary_keys, keep=False)]
    unique_df = df.drop_duplicates(subset=primary_keys)
    return duplicates, unique_df


def upsert_chunk(args):
    """데이터베이스 테이블에 데이터 청크를 병합(Upsert)합니다.

    Args:
        args (tuple): 다음 요소들을 포함한 튜플.
            - chunk (pd.DataFrame): 삽입 또는 업데이트할 데이터 청크.
            - table_name (str): 데이터가 삽입될 데이터베이스 테이블의 이름.
            - primary_keys (list): 중복을 식별할 기본 키 열의 리스트.

    Notes:
        이 함수는 PostgreSQL의 "ON CONFLICT" 절을 사용하여 중복된 키가 있을 경우 데이터를 업데이트하고,
        그렇지 않으면 새로 삽입하는 동작을 수행합니다.

        `session.begin()` 블록 내에서 트랜잭션이 자동으로 관리됩니다.
        중복된 기본 키에 대해 업데이트가 발생하며, 기본 키 열은 업데이트되지 않습니다.

        데이터베이스 작업이 완료되면 트랜잭션을 커밋하고 세션을 닫습니다.
    """
    engine = connect_db()
    metadata = MetaData()
    
    chunk, table_name, primary_keys = args
    table = Table(table_name, metadata, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with session.begin():  # 트랜잭션을 시작합니다.
        insert_stmt = pg_insert(table).values(chunk)  # 삽입할 데이터를 준비합니다.
        update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=primary_keys,  # 충돌 시 확인할 기본 키 열을 지정합니다.
            set_={
                c.name: c for c in insert_stmt.excluded if c.name not in primary_keys
            },  # 기본 키를 제외한 열들을 업데이트합니다.
        )
        session.execute(update_stmt)  # SQL 문을 실행합니다.

    session.commit()  # 트랜잭션을 커밋합니다.
    session.close()  # 세션을 종료합니다.


def upsert_data(df, table, primary_keys, chunk_size=1000):
    """데이터프레임을 데이터베이스 테이블에 병합(Upsert)합니다.

    Args:
        df (pd.DataFrame): 삽입 또는 업데이트할 데이터를 포함한 데이터프레임.
        table (sqlalchemy.Table): 데이터가 삽입될 데이터베이스 테이블 객체.
        primary_keys (list): 중복을 식별할 기본 키 열의 리스트.
        chunk_size (int, optional): 한 번에 처리할 데이터 청크의 크기. 기본값은 1000.
    """
    table_name = table.name

    # 데이터프레임에서 중복된 레코드를 감지하고 제거합니다.
    duplicates, unique_df = detect_and_remove_duplicates(df, primary_keys)

    # 중복된 레코드를 CSV 파일로 저장합니다.
    duplicates.to_csv(f"out/duplicates_{table.name}.csv", index=False)

    # 데이터프레임을 청크로 나눕니다.
    chunks = [
        unique_df.iloc[i : i + chunk_size].to_dict(orient="records")
        for i in range(0, len(unique_df), chunk_size)
    ]

    total_chunks = len(chunks)

    # 병렬로 청크를 병합(Upsert)합니다.
    with Pool(processes=cpu_count()) as pool:
        for i, _ in enumerate(
            pool.imap_unordered(
                upsert_chunk, [(chunk, table_name, primary_keys) for chunk in chunks]
            ),
            1,
        ):
            logging.info(
                f"Processing chunk {i}/{total_chunks} for table [{table.name}]"
            )

    logging.info(
        f"Upsert completed for table [{table.name}] with {total_chunks} chunks."
    )


def upload_csv(file_path, table_name, primary_keys, foreign_keys=None, option=[]):
    """CSV 파일을 데이터베이스 테이블에 업로드하고, 필요시 테이블을 초기화 및 데이터 병합(Upsert)합니다.

    Args:
        file_path (str): 업로드할 CSV 파일의 경로.
        table_name (str): 데이터가 업로드될 데이터베이스 테이블의 이름.
        primary_keys (list): 중복을 식별할 기본 키 열의 리스트.
        foreign_keys (dict, optional): 외래 키 관계를 정의하는 딕셔너리. 기본값은 None.
        option (list, optional): 추가 옵션 리스트. 'reset'이 포함된 경우 테이블을 초기화합니다. 기본값은 빈 리스트.

    Notes:
        이 함수는 다음 작업을 수행합니다:
        1. CSV 파일을 로드하여 데이터프레임으로 변환합니다.
        2. 데이터베이스에 테이블을 생성합니다. 외래 키가 제공된 경우 이를 포함합니다.
        3. 'reset' 옵션이 제공된 경우, 기존 테이블을 초기화합니다.
        4. 데이터프레임의 데이터를 테이블에 병합(Upsert)합니다.
    """
    logging.info("Process started.")

    logging.info("Loading dataframe...")
    df = pd.read_csv(file_path)

    logging.info("Generating table...")
    table = create_table_from_csv(df, table_name, primary_keys, foreign_keys)

    if "reset" in option:
        logging.info("Clearing table...")
        clear_table(table.name)

    logging.info("Upserting data...")
    upsert_data(df, table, primary_keys)

