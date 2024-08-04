from ultralytics import YOLO

model = YOLO('yolov8s-seg.yaml').load('yolov8s-seg.pt')  # build from YAML and transfer weights
training_results = model.train(data="config.yaml", task="segment", device=8)  # train the model
metrics = model.val()  # evaluate model performance on the validation set
print("Training Results .....")
print(training_results)
print("Metrics")
print(metrics)


# yolo detect train data=coco8-seg.yaml model=yolov8n-seg.pt epochs=100 imgsz=640 # training with CLI
