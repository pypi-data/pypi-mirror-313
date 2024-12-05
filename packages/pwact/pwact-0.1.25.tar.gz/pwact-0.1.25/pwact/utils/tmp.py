from pwdata import Config
import os, sys, glob
import numpy as np

def count_pwdata():
    work_dir = "/data/home/wuxingxing/datas/debugs/dengjiapei/run_iter/mlmd_pwdata"
    dir_list = glob.glob(os.path.join(work_dir, "*"))
    res = []
    for dir in dir_list:
        # train
        train_num = np.load(os.path.join(dir, "train/energies.npy")).shape[0]
        res.append(train_num)

        if os.path.exists(os.path.join(dir, "valid/energies.npy")):
            test_num = np.load(os.path.join(dir, "valid/energies.npy")).shape[0]
            res.append(test_num)
            print("{} {} {}".format( dir, train_num, test_num))
        else:
            print("{} {}".format(dir, train_num))
    print(np.sum(res))

def count_outmlmd():
    work_dir = "/data/home/wuxingxing/datas/debugs/dengjiapei/run_iter/iter.0000/label/scf"
    mlmds = glob.glob(os.path.join(work_dir, "*/*/*/OUT.MLMD"))
    print(len(mlmds))

def save_mlmd():
    work_dir = "/data/home/wuxingxing/datas/debugs/dengjiapei/run_iter"
    data_list = glob.glob(os.path.join(work_dir, "iter.*/label/scf/*/*/*/OUT.MLMD"))
    datasets_path = "/data/home/wuxingxing/datas/debugs/dengjiapei/run_iter/mlmd_pwdata"
    # data_name = datasets_path
    image_data = None
    for data_path in data_list:
        if image_data is not None:
            tmp_config = Config("pwmat/movement", data_path)
            # if not isinstance(tmp_config, list):
            #     tmp_config = [tmp_config]
            image_data.images.extend(tmp_config.images)
        else:
            image_data = Config("pwmat/movement", data_path)
            
            if not isinstance(image_data.images, list):
                image_data.images = [image_data.images]
        
            # if not isinstance(image_data, list):
            #     image_data = [image_data]
    image_data.to(
                output_path=datasets_path,
                save_format="pwmlff/npy",
                train_ratio = 0.8, 
                train_data_path="train", 
                valid_data_path="valid", 
                random=True,
                seed = 2024, 
                retain_raw = False
                )
    print(len(image_data.images))


if __name__=="__main__":
    count_pwdata()
    # count_outmlmd()
    # save_mlmd()