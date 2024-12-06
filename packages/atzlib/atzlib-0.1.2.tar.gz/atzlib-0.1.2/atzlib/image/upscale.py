import cv2
import os

def upscale_image(input_path, output_path, scale_factor):
    """
    Upscale Image.

    Args:
        input_path (path): 입력파일 경로
        output_path (path): 출력파일 경로
        scale_factor (int): 2, 3, 4 중 선택. EDSR 모델 선택 결정.
    """
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    cur_path = os.path.dirname(__file__)
    model_path = f"EDSR_x{scale_factor}.pb"
    
    path = os.path.join(cur_path, model_path)
    
    sr.readModel(path)
    sr.setModel("edsr", scale_factor)
    
    img = cv2.imread(input_path)
    result = sr.upsample(img)
    cv2.imwrite(output_path, result)


def batch_upscale(input_folder, output_folder, scale_factor):
    """
    배치(폴더) 단위로 이미지 업스케일링 수행.

    Args:
        input_folder (path): 입력폴더
        output_folder (path): 출력폴더
        scale_factor (float): 배율(2, 3, 4)
    """
    # 입력 폴더의 모든 파일을 순회
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # 이미지 파일일 경우
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # 이미지 업스케일링
            upscale_image(input_path, output_path, scale_factor)

if __name__ == "__main__":
    # 사용 예시
    input_folder = 'input'  # 입력 이미지 폴더 경로
    output_folder = 'output'  # 출력 이미지 폴더 경로
    scale_factor = 2  # 이미지 배율

    # 출력 폴더가 없다면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    batch_upscale(input_folder, output_folder, scale_factor)
