import os

def ensure_storage_directory_exists(config):
    """check storege"""
    os.makedirs(config.MAIN_PATH, exist_ok=True)
    os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}", exist_ok=True)
    os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}", exist_ok=True)
    os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}", exist_ok=True)
    os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}", exist_ok=True)
    os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.IMAGE_PATH}/{config.THUMBNAIL_PATH}", exist_ok=True)

#     if not os.path.exists(config.MAIN_PATH):
#         os.makedirs(config.MAIN_PATH)
#         print(f"create {config.MAIN_PATH} success !!!!")
#         check_sub_path(config)
#     else:
#         print(f"directory {config.MAIN_PATH} is already")
#         check_sub_path(config)

# def check_sub_path(config):
#     """check sub path"""
#     if not os.path.exists(f"{config.MAIN_PATH}/{config.SUB_PATH}"):
#         os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}")
#         print(f"create {config.MAIN_PATH}/{config.SUB_PATH} success !!!!")
#         check_upload_path(config)
#     else:
#         print(f"directory {config.MAIN_PATH}/{config.SUB_PATH} is already")
#         check_upload_path(config)

# def check_upload_path(config):
#     """check upload path"""
#     if not os.path.exists(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}"):
#         os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS}")
#         print(f"create {config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS} success !!!!")
#         check_hls_path(config)
#     else:
#         print(f"directory {config.MAIN_PATH}/{config.SUB_PATH}/{config.UPLOAD_DIR_HLS} is already")
#         check_hls_path(config)

# def check_hls_path(config):
#     """check hls path"""
#     if not os.path.exists(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}"):
#         os.makedirs(f"{config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR}")
#         print(f"create {config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR} success !!!!")
#     else:
#         print(f"directory {config.MAIN_PATH}/{config.SUB_PATH}/{config.HLS_DIR} is already")