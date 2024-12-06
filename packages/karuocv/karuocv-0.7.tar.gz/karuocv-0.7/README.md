# KARUOCV

> package for computer vision tools wrap



## command usage:
usage: karuocv [-h] --task TASK [--base_model BASE_MODEL] [--device DEVICE] [--epochs EPOCHS] [--iterations ITERATIONS] [--batch_size BATCH_SIZE] [--path PATH] [--verbose] [--format FORMAT]
               [--source_a SOURCE_A] [--source_b SOURCE_B] [--dest DEST]

SACP object train tools

options:
  -h, --help            show this help message and exit  
  --task TASK           指定任务 train, inference, mix_datasets, ETC  
  --base_model BASE_MODEL
                        底座模型的路径  
  --device DEVICE       select one in the list which contains cpu, cuda and mps  
  --epochs EPOCHS       训练迭代周期  
  --iterations ITERATIONS
                        The number of generations to run the evolution for.  
  --batch_size BATCH_SIZE
                        the batch size of train.  
  --path PATH           some path parameter.  
  --verbose             show log for inference or not  
  --format FORMAT       format parameter  
  --source_a SOURCE_A  
  --source_b SOURCE_B  
  --dest DEST           the output files destnation path.  
  --imshow              是否通过cv2显示图片  