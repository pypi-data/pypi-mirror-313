"""
maix.nn module
"""
from __future__ import annotations
import maix._maix.err
import maix._maix.image
import maix._maix.tensor
import typing
from . import F
__all__ = ['Classifier', 'F', 'FaceDetector', 'FaceObject', 'FaceObjects', 'FaceRecognizer', 'LayerInfo', 'MUD', 'NN', 'NanoTrack', 'OCR_Box', 'OCR_Object', 'OCR_Objects', 'Object', 'ObjectFloat', 'Objects', 'PP_OCR', 'Retinaface', 'SelfLearnClassifier', 'Speech', 'SpeechDecoder', 'SpeechDevice', 'YOLO11', 'YOLOv5', 'YOLOv8']
class Classifier:
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def classify(self, img: maix._maix.image.Image, softmax: bool = True, fit: maix._maix.image.Fit = ...) -> list[tuple[int, float]]:
        """
        Forward image to model, get result. Only for image input, use classify_raw for tensor input.
        
        Args:
          - img: image, format should match model input_type， or will raise err.Exception
          - softmax: if true, will do softmax to result, or will return raw value
          - fit: image resize fit mode, default Fit.FIT_COVER, see image.Fit.
        
        
        Returns: result, a list of (label, score). If in dual_buff mode, value can be one element list and score is zero when not ready. In C++, you need to delete it after use.
        """
    def classify_raw(self, data: maix._maix.tensor.Tensor, softmax: bool = True) -> list[tuple[int, float]]:
        """
        Forward tensor data to model, get result
        
        Args:
          - data: tensor data, format should match model input_type， or will raise err.Excetion
          - softmax: if true, will do softmax to result, or will return raw value
        
        
        Returns: result, a list of (label, score). In C++, you need to delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format, only for image input
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height, only for image input
        
        Returns: model input size of height
        """
    def input_shape(self) -> list[int]:
        """
        Get input shape, if have multiple input, only return first input shape
        
        Returns: input shape, list type
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size, only for image input
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width, only for image input
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file, model format is .mud,
        MUD file should contain [extra] section, have key-values:
        - model_type: classifier
        - input_type: rgb or bgr
        - mean: 123.675, 116.28, 103.53
        - scale: 0.017124753831663668, 0.01750700280112045, 0.017429193899782137
        - labels: imagenet_classes.txt
        
        Args:
          - model: MUD model path
        
        
        Returns: error code, if load failed, return error code
        """
class FaceDetector:
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, fit: maix._maix.image.Fit = ...) -> list[Object]:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.5.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
        
        
        Returns: Object list. In C++, you should delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
class FaceObject:
    class_id: int
    face: maix._maix.image.Image
    feature: list[float]
    h: int
    points: list[int]
    score: float
    w: int
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, class_id: int = 0, score: float = 0, points: list[int] = [], feature: list[float] = [], face: maix._maix.image.Image = ...) -> None:
        ...
    def __str__(self) -> str:
        """
        FaceObject info to string
        
        Returns: FaceObject info string
        """
class FaceObjects:
    def __getitem__(self, idx: int) -> FaceObject:
        """
        Get object item
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        """
        Get size
        """
    def add(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, class_id: int = 0, score: float = 0, points: list[int] = [], feature: list[float] = [], face: maix._maix.image.Image = ...) -> FaceObject:
        """
        Add object to FaceObjects
        """
    def at(self, idx: int) -> FaceObject:
        """
        Get object item
        """
    def remove(self, idx: int) -> maix._maix.err.Err:
        """
        Remove object form FaceObjects
        """
class FaceRecognizer:
    features: list[list[float]]
    labels: list[str]
    mean_detector: list[float]
    mean_feature: list[float]
    scale_detector: list[float]
    scale_feature: list[float]
    def __init__(self, detect_model: str = '', feature_model: str = '', dual_buff: bool = True) -> None:
        ...
    def add_face(self, face: FaceObject, label: str) -> maix._maix.err.Err:
        """
        Add face to lib
        
        Args:
          - face: face object, find by recognize
          - label: face label(name)
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, detect_model: str, feature_model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - detect_model: face detect model path, default empty, you can load model later by load function.
          - feature_model: feature extract model
        
        
        Returns: err::Err
        """
    def load_faces(self, path: str) -> maix._maix.err.Err:
        """
        Load faces info from a file
        
        Args:
          - path: from where to load, string type.
        
        
        Returns: err::Err type
        """
    def recognize(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, compare_th: float = 0.8, get_feature: bool = False, get_face: bool = False, fit: maix._maix.image.Fit = ...) -> FaceObjects:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Detect confidence threshold, default 0.5.
          - iou_th: Detect IoU threshold, default 0.45.
          - compare_th: Compare two face score threshold, default 0.8, if two faces' score < this value, will see this face fas unknown.
          - get_feature: return feature or not, if true will copy features to result, if false will not copy feature to result to save time and memory.
          - get_face: return face image or not, if true result object's face attribute will valid, or face sttribute is empty. Get face image will alloc memory and copy image, so will lead to slower speed.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
        
        
        Returns: FaceObjects object. In C++, you should delete it after use.
        """
    def remove_face(self, idx: int = -1, label: str = '') -> maix._maix.err.Err:
        """
        remove face from lib
        
        Args:
          - idx: index of face in lib, default -1 means use label, value [0,face_num), idx and label must have one, idx have high priotiry.
          - label: which face to remove, default to empty string mean use idx, idx and label must have one, idx have high priotiry.
        """
    def save_faces(self, path: str) -> maix._maix.err.Err:
        """
        Save faces info to a file
        
        Args:
          - path: where to save, string type.
        
        
        Returns: err.Err type
        """
class LayerInfo:
    dtype: maix._maix.tensor.DType
    name: str
    shape: list[int]
    def __init__(self, name: str = '', dtype: maix._maix.tensor.DType = ..., shape: list[int] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        To string
        """
    def shape_int(self) -> int:
        """
        Shape as one int type, multiply all dims of shape
        """
    def to_str(self) -> str:
        """
        To string
        """
class MUD:
    items: dict[str, dict[str, str]]
    type: str
    def __init__(self, model_path: str = None) -> None:
        ...
    def load(self, model_path: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model_path: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
class NN:
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def extra_info(self) -> dict[str, str]:
        """
        Get model extra info define in MUD file
        
        Returns: extra info, dict type, key-value object, attention: key and value are all string type.
        """
    def forward(self, inputs: maix._maix.tensor.Tensors, copy_result: bool = True, dual_buff_wait: bool = False) -> maix._maix.tensor.Tensors:
        """
        forward run model, get output of model,
        this is specially for MaixPy, not efficient, but easy to use in MaixPy
        
        Args:
          - input: direction [in], input tensor
          - copy_result: If set true, will copy result to a new variable; else will use a internal memory, you can only use it until to the next forward.
        Default true to avoid problems, you can set it to false manually to make speed faster.
          - dual_buff_wait: bool type, only for dual_buff mode, if true, will inference this image and wait for result, default false.
        
        
        Returns: output tensor. In C++, you should manually delete tensors in return value and return value.
        If dual_buff mode, it can be NULL(None in MaixPy) means not ready.
        """
    def forward_image(self, img: maix._maix.image.Image, mean: list[float] = [], scale: list[float] = [], fit: maix._maix.image.Fit = ..., copy_result: bool = True, dual_buff_wait: bool = False) -> maix._maix.tensor.Tensors:
        """
        forward model, param is image
        
        Args:
          - img: input image
          - mean: mean value, a list type, e.g. [0.485, 0.456, 0.406], default is empty list means not normalize.
          - scale: scale value, a list type, e.g. [1/0.229, 1/0.224, 1/0.225], default is empty list means not normalize.
          - fit: fit mode, if the image size of input not equal to model's input, it will auto resize use this fit method,
        default is image.Fit.FIT_FILL for easy coordinate calculation, but for more accurate result, use image.Fit.FIT_CONTAIN is better.
          - copy_result: If set true, will copy result to a new variable; else will use a internal memory, you can only use it until to the next forward.
        Default true to avoid problems, you can set it to false manually to make speed faster.
          - dual_buff_wait: bool type, only for dual_buff mode, if true, will inference this image and wait for result, default false.
        
        
        Returns: output tensor. In C++, you should manually delete tensors in return value and return value.
        If dual_buff mode, it can be NULL(None in MaixPy) means not ready.
        """
    def inputs_info(self) -> list[LayerInfo]:
        """
        Get model input layer info
        
        Returns: input layer info
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: direction [in], model file path, model format can be MUD(model universal describe file) file.
        
        
        Returns: error code, if load success, return err::ERR_NONE
        """
    def loaded(self) -> bool:
        """
        Is model loaded
        
        Returns: true if model loaded, else false
        """
    def outputs_info(self) -> list[LayerInfo]:
        """
        Get model output layer info
        
        Returns: output layer info
        """
    def set_dual_buff(self, enable: bool) -> None:
        """
        Enable dual buff or disable dual buff
        
        Args:
          - enable: true to enable, false to disable
        """
class NanoTrack:
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '') -> None:
        ...
    def init(self, img: maix._maix.image.Image, x: int, y: int, w: int, h: int) -> None:
        """
        Init tracker, give tacker first target image and target position.
        
        Args:
          - img: Image want to detect, target should be in this image.
          - x: the target position left top coordinate x.
          - y: the target position left top coordinate y.
          - w: the target width.
          - h: the target height.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
    def track(self, img: maix._maix.image.Image, threshold: float = 0.9) -> ...:
        """
        Track object acoording to last object position and the init function learned target feature.
        
        Args:
          - img: image to detect object and track, can be any resolution, before detect it will crop a area according to last time target's position.
          - threshold: If score < threshold, will see this new detection is invalid, but remain return this new detecion,  default 0.9.
        
        
        Returns: object, position and score, and detect area in points's first 4 element(x, y, w, h, center_x, center_y, input_size, target_size)
        """
class OCR_Box:
    x1: int
    x2: int
    x3: int
    x4: int
    y1: int
    y2: int
    y3: int
    y4: int
    def __init__(self, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0, x3: int = 0, y3: int = 0, x4: int = 0, y4: int = 0) -> None:
        ...
    def to_list(self) -> list[int]:
        """
        convert box point to a list type.
        
        Returns: list type, element is int type, value [x1, y1, x2, y2, x3, y3, x4, y4].
        """
class OCR_Object:
    box: OCR_Box
    char_pos: list[int]
    idx_list: list[int]
    score: float
    def __init__(self, box: OCR_Box, idx_list: list[int], char_list: list[str], score: float = 0, char_pos: list[int] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        OCR_Object info to string
        
        Returns: OCR_Object info string
        """
    def char_list(self) -> list[str]:
        """
        Get OCR_Object's charactors, return a list type.
        
        Returns: All charactors in list type.
        """
    def char_str(self) -> str:
        """
        Get OCR_Object's charactors, return a string type.
        
        Returns: All charactors in string type.
        """
    def update_chars(self, char_list: list[str]) -> None:
        """
        Set OCR_Object's charactors
        
        Args:
          - char_list: All charactors in list type.
        """
class OCR_Objects:
    def __getitem__(self, idx: int) -> OCR_Object:
        """
        Get object item
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        """
        Get size
        """
    def add(self, box: OCR_Box, idx_list: list[int], char_list: list[str], score: float = 0, char_pos: list[int] = []) -> OCR_Object:
        """
        Add object to objects
        """
    def at(self, idx: int) -> OCR_Object:
        """
        Get object item
        """
    def remove(self, idx: int) -> maix._maix.err.Err:
        """
        Remove object form objects
        """
class Object:
    class_id: int
    h: int
    points: list[int]
    score: float
    seg_mask: maix._maix.image.Image
    w: int
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, class_id: int = 0, score: float = 0, points: list[int] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        Object info to string
        
        Returns: Object info string
        """
class ObjectFloat:
    class_id: float
    h: float
    points: list[float]
    score: float
    w: float
    x: float
    y: float
    def __init__(self, x: float = 0, y: float = 0, w: float = 0, h: float = 0, class_id: float = 0, score: float = 0, points: list[float] = []) -> None:
        ...
    def __str__(self) -> str:
        """
        Object info to string
        
        Returns: Object info string
        """
class Objects:
    def __getitem__(self, idx: int) -> Object:
        """
        Get object item
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator:
        ...
    def __len__(self) -> int:
        """
        Get size
        """
    def add(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0, class_id: int = 0, score: float = 0, points: list[int] = []) -> Object:
        """
        Add object to objects
        """
    def at(self, idx: int) -> Object:
        """
        Get object item
        """
    def remove(self, idx: int) -> maix._maix.err.Err:
        """
        Remove object form objects
        """
class PP_OCR:
    det: bool
    labels: list[str]
    mean: list[float]
    rec: bool
    rec_mean: list[float]
    rec_scale: list[float]
    scale: list[float]
    def __init__(self, model: str = '') -> None:
        ...
    def detect(self, img: maix._maix.image.Image, thresh: float = 0.3, box_thresh: float = 0.6, fit: maix._maix.image.Fit = ..., char_box: bool = False) -> OCR_Objects:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - thresh: Confidence threshold where pixels have charactor, default 0.3.
          - box_thresh: Box threshold, the box prob higher than this value will be valid, default 0.6.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
          - char_box: Calculate every charactor's box, default false, if true then you can get charactor's box by nn.OCR_Object's char_boxes attribute.
        
        
        Returns: nn.OCR_Objects type. In C++, you should delete it after use.
        """
    def draw_seg_mask(self, img: maix._maix.image.Image, x: int, y: int, seg_mask: maix._maix.image.Image, threshold: int = 127) -> None:
        """
        Draw segmentation on image
        
        Args:
          - img: image object, maix.image.Image type.
          - seg_mask: segmentation mask image by detect method, a grayscale image
          - threshold: only mask's value > threshold will be draw on image, value from 0 to 255.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
    def recognize(self, img: maix._maix.image.Image, box_points: list[int] = []) -> OCR_Object:
        """
        Only recognize, not detect
        
        Args:
          - img: image to recognize chractors, can be a stanrd cropped charactors image,
        if crop image not standard, you can use box_points to assgin where the charactors' 4 corner is.
          - box_points: list type, length must be 8 or 0, default empty means not transfer image to standard image.
        4 points postiion, format: [x1, y1, x2, y2, x3, y3, x4, y4], point 1 at the left-top, point 2 right-top...
          - char_box: Calculate every charactor's box, default false, if true then you can get charactor's box by nn.OCR_Object's char_boxes attribute.
        """
class Retinaface:
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.4, iou_th: float = 0.45, fit: maix._maix.image.Fit = ...) -> list[Object]:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.4.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
        
        
        Returns: Object list. In C++, you should delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
class SelfLearnClassifier:
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def add_class(self, img: maix._maix.image.Image, fit: maix._maix.image.Fit = ...) -> None:
        """
        Add a class to recognize
        
        Args:
          - img: Add a image as a new class
          - fit: image resize fit mode, default Fit.FIT_COVER, see image.Fit.
        """
    def add_sample(self, img: maix._maix.image.Image, fit: maix._maix.image.Fit = ...) -> None:
        """
        Add sample, you should call learn method after add some samples to learn classes.
        Sample image can be any of classes we already added.
        
        Args:
          - img: Add a image as a new sample.
        """
    def class_num(self) -> int:
        """
        Get class number
        """
    def classify(self, img: maix._maix.image.Image, fit: maix._maix.image.Fit = ...) -> list[tuple[int, float]]:
        """
        Classify image
        
        Args:
          - img: image, format should match model input_type， or will raise err.Exception
          - fit: image resize fit mode, default Fit.FIT_COVER, see image.Fit.
        
        
        Returns: result, a list of (idx, distance), smaller distance means more similar. In C++, you need to delete it after use.
        """
    def clear(self) -> None:
        """
        Clear all class and samples
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format, only for image input
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height, only for image input
        
        Returns: model input size of height
        """
    def input_shape(self) -> list[int]:
        """
        Get input shape, if have multiple input, only return first input shape
        
        Returns: input shape, list type
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size, only for image input
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width, only for image input
        
        Returns: model input size of width
        """
    def learn(self) -> int:
        """
        Start auto learn class features from classes image and samples.
        You should call this method after you add some samples.
        
        Returns: learn epoch(times), 0 means learn nothing.
        """
    def load(self, path: str) -> list[str]:
        """
        Load features info from binary file
        
        Args:
          - path: feature info binary file path, e.g. /root/my_classes.bin
        """
    def load_model(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file, model format is .mud,
        MUD file should contain [extra] section, have key-values:
        - model_type: classifier_no_top
        - input_type: rgb or bgr
        - mean: 123.675, 116.28, 103.53
        - scale: 0.017124753831663668, 0.01750700280112045, 0.017429193899782137
        
        Args:
          - model: MUD model path
        
        
        Returns: error code, if load failed, return error code
        """
    def rm_class(self, idx: int) -> maix._maix.err.Err:
        """
        Remove a class
        
        Args:
          - idx: index, value from 0 to class_num();
        """
    def rm_sample(self, idx: int) -> maix._maix.err.Err:
        """
        Remove a sample
        
        Args:
          - idx: index, value from 0 to sample_num();
        """
    def sample_num(self) -> int:
        """
        Get sample number
        """
    def save(self, path: str, labels: list[str] = []) -> maix._maix.err.Err:
        """
        Save features and labels to a binary file
        
        Args:
          - path: file path to save, e.g. /root/my_classes.bin
          - labels: class labels, can be None, or length must equal to class num, or will return err::Err
        
        
        Returns: maix.err.Err if labels exists but length not equal to class num, or save file failed, or class num is 0.
        """
class Speech:
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '') -> None:
        ...
    def clear(self) -> None:
        """
        Reset internal cache operation
        """
    def dec_deinit(self, decoder: SpeechDecoder) -> None:
        """
        Deinit the decoder.
        
        Args:
          - decoder: decoder type want to deinit
        can choose between DECODER_RAW, DECODER_DIG, DECODER_LVCSR, DECODER_KWS or DECODER_ALL.
        """
    def dev_type(self) -> SpeechDevice:
        """
        get device type
        
        Returns: nn::SpeechDevice type, see SpeechDevice of this module
        """
    def devive(self, dev_type: SpeechDevice, device_name: str) -> maix._maix.err.Err:
        """
        Reset the device, usually used for PCM/WAV recognition,
        such as identifying the next WAV file.
        
        Args:
          - dev_type: device type want to detect, can choose between WAV, PCM, or MIC.
          - device_name: device name want to detect, can choose a WAV file, a PCM file, or a MIC device name.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def digit(self, blank: int, callback: typing.Callable[[str, int], None]) -> maix._maix.err.Err:
        """
        Init digit decoder, it will output the Chinese digit recognition results within the last 4 seconds.
        
        Args:
          - blank: If it exceeds this value, insert a '_' in the output result to indicate idle mute.
          - callback: digit decoder user callback.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def frame_time(self) -> int:
        """
        Get the time of one frame.
        
        Returns: int type, return the time of one frame.
        """
    def init(self, dev_type: SpeechDevice, device_name: str = '') -> maix._maix.err.Err:
        """
        Init the ASR library and select the type and name of the audio device.
        
        Args:
          - dev_type: device type want to detect, can choose between WAV, PCM, or MIC.
          - device_name: device name want to detect, can choose a WAV file, a PCM file, or a MIC device name.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def kws(self, kw_tbl: list[str], kw_gate: list[float], callback: typing.Callable[[list[float], int], None], auto_similar: bool = True) -> maix._maix.err.Err:
        """
        Init kws decoder, it will output a probability list of all registered keywords in the latest frame,
        users can set their own thresholds for wake-up.
        
        Args:
          - kw_tbl: Keyword list, filled in with spaces separated by pinyin, for example: xiao3 ai4 tong2 xue2
          - kw_gate: kw_gate, keyword probability gate table, the number should be the same as kw_tbl
          - auto_similar: Whether to perform automatic homophone processing,
        setting it to true will automatically calculate the probability by using pinyin with different tones as homophones
          - callback: digit decoder user callback.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
    def lvcsr(self, sfst_name: str, sym_name: str, phones_txt: str, words_txt: str, callback: typing.Callable[[tuple[str, str], int], None], beam: float = 8, bg_prob: float = 10, scale: float = 0.5, mmap: bool = False) -> maix._maix.err.Err:
        """
        Init lvcsr decoder, it will output continuous speech recognition results (less than 1024 Chinese characters).
        
        Args:
          - sfst_name: Sfst file path.
          - sym_name: Sym file path (output symbol table).
          - phones_txt: Path to phones.bin (pinyin table).
          - words_txt: Path to words.bin (dictionary table).
          - callback: lvcsr decoder user callback.
          - beam: The beam size for WFST search is set to 8 by default, and it is recommended to be between 3 and 9.
        The larger the size, the larger the search space, and the more accurate but slower the search.
          - bg_prob: The absolute value of the natural logarithm of the default probability value for background pinyin
        outside of BEAM-CNT is set to 10 by default.
          - scale: acoustics_cost = log(pny_prob)*scale.
          - mmap: use mmap to load the WFST decoding image,
        If set to true, the beam should be less than 5.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def raw(self, callback: typing.Callable[[list[tuple[int, float]], int], None]) -> maix._maix.err.Err:
        """
        Init raw decoder, it will output the prediction results of the original AM.
        
        Args:
          - callback: raw decoder user callback.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def run(self, frame: int) -> int:
        """
        Run speech recognition, user can run 1 frame at a time and do other processing after running,
        or it can run continuously within a thread and be stopped by an external thread.
        
        Args:
          - frame: The number of frames per run.
        
        
        Returns: int type, return actual number of frames in the run.
        """
    def similar(self, pny: str, similar_pnys: list[str]) -> maix._maix.err.Err:
        """
        Manually register mute words, and each pinyin can register up to 10 homophones,
        please note that using this interface to register homophones will overwrite,
        the homophone table automatically generated in the "automatic homophone processing" feature.
        
        Args:
          - dev_type: device type want to detect, can choose between WAV, PCM, or MIC.
          - device_name: device name want to detect, can choose a WAV file, a PCM file, or a MIC device name.
        
        
        Returns: err::Err type, if init success, return err::ERR_NONE
        """
    def skip_frames(self, num: int) -> None:
        """
        Run some frames and drop, this can be used to avoid
        incorrect recognition results when switching decoders.
        
        Args:
          - num: number of frames to run and drop
        """
class SpeechDecoder:
    """
    Members:
    
      DECODER_RAW
    
      DECODER_DIG
    
      DECODER_LVCSR
    
      DECODER_KWS
    
      DECODER_ALL
    """
    DECODER_ALL: typing.ClassVar[SpeechDecoder]  # value = <SpeechDecoder.DECODER_ALL: 65535>
    DECODER_DIG: typing.ClassVar[SpeechDecoder]  # value = <SpeechDecoder.DECODER_DIG: 2>
    DECODER_KWS: typing.ClassVar[SpeechDecoder]  # value = <SpeechDecoder.DECODER_KWS: 8>
    DECODER_LVCSR: typing.ClassVar[SpeechDecoder]  # value = <SpeechDecoder.DECODER_LVCSR: 4>
    DECODER_RAW: typing.ClassVar[SpeechDecoder]  # value = <SpeechDecoder.DECODER_RAW: 1>
    __members__: typing.ClassVar[dict[str, SpeechDecoder]]  # value = {'DECODER_RAW': <SpeechDecoder.DECODER_RAW: 1>, 'DECODER_DIG': <SpeechDecoder.DECODER_DIG: 2>, 'DECODER_LVCSR': <SpeechDecoder.DECODER_LVCSR: 4>, 'DECODER_KWS': <SpeechDecoder.DECODER_KWS: 8>, 'DECODER_ALL': <SpeechDecoder.DECODER_ALL: 65535>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SpeechDevice:
    """
    Members:
    
      DEVICE_NONE
    
      DEVICE_PCM
    
      DEVICE_MIC
    
      DEVICE_WAV
    """
    DEVICE_MIC: typing.ClassVar[SpeechDevice]  # value = <SpeechDevice.DEVICE_MIC: 1>
    DEVICE_NONE: typing.ClassVar[SpeechDevice]  # value = <SpeechDevice.DEVICE_NONE: -1>
    DEVICE_PCM: typing.ClassVar[SpeechDevice]  # value = <SpeechDevice.DEVICE_PCM: 0>
    DEVICE_WAV: typing.ClassVar[SpeechDevice]  # value = <SpeechDevice.DEVICE_WAV: 2>
    __members__: typing.ClassVar[dict[str, SpeechDevice]]  # value = {'DEVICE_NONE': <SpeechDevice.DEVICE_NONE: -1>, 'DEVICE_PCM': <SpeechDevice.DEVICE_PCM: 0>, 'DEVICE_MIC': <SpeechDevice.DEVICE_MIC: 1>, 'DEVICE_WAV': <SpeechDevice.DEVICE_WAV: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class YOLO11:
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, fit: maix._maix.image.Fit = ..., keypoint_th: float = 0.5) -> Objects:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.5.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
          - keypoint_th: keypoint threshold, default 0.5, only for yolo11-pose model.
        
        
        Returns: Object list. In C++, you should delete it after use.
        If model is yolo11-pose, object's points have value, and if points' value < 0 means that point is invalid(conf < keypoint_th).
        """
    def draw_pose(self, img: maix._maix.image.Image, points: list[int], radius: int = 4, color: maix._maix.image.Color = ..., body: bool = True) -> None:
        """
        Draw pose keypoints on image
        
        Args:
          - img: image object, maix.image.Image type.
          - points: keypoits, int list type, [x, y, x, y ...]
          - radius: radius of points.
          - color: color of points.
          - body: true, if points' length is 17*2 and body is ture, will draw lines as human body, if set to false won't draw lines, default true.
        """
    def draw_seg_mask(self, img: maix._maix.image.Image, x: int, y: int, seg_mask: maix._maix.image.Image, threshold: int = 127) -> None:
        """
        Draw segmentation on image
        
        Args:
          - img: image object, maix.image.Image type.
          - seg_mask: segmentation mask image by detect method, a grayscale image
          - threshold: only mask's value > threshold will be draw on image, value from 0 to 255.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
class YOLOv5:
    anchors: list[float]
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, fit: maix._maix.image.Fit = ...) -> list[Object]:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.5.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
        
        
        Returns: Object list. In C++, you should delete it after use.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
class YOLOv8:
    label_path: str
    labels: list[str]
    mean: list[float]
    scale: list[float]
    def __init__(self, model: str = '', dual_buff: bool = True) -> None:
        ...
    def detect(self, img: maix._maix.image.Image, conf_th: float = 0.5, iou_th: float = 0.45, fit: maix._maix.image.Fit = ..., keypoint_th: float = 0.5) -> ...:
        """
        Detect objects from image
        
        Args:
          - img: Image want to detect, if image's size not match model input's, will auto resize with fit method.
          - conf_th: Confidence threshold, default 0.5.
          - iou_th: IoU threshold, default 0.45.
          - fit: Resize method, default image.Fit.FIT_CONTAIN.
          - keypoint_th: keypoint threshold, default 0.5, only for yolov8-pose model.
        
        
        Returns: Object list. In C++, you should delete it after use.
        If model is yolov8-pose, object's points have value, and if points' value < 0 means that point is invalid(conf < keypoint_th).
        """
    def draw_pose(self, img: maix._maix.image.Image, points: list[int], radius: int = 4, color: maix._maix.image.Color = ..., body: bool = True) -> None:
        """
        Draw pose keypoints on image
        
        Args:
          - img: image object, maix.image.Image type.
          - points: keypoits, int list type, [x, y, x, y ...]
          - radius: radius of points.
          - color: color of points.
          - body: true, if points' length is 17*2 and body is ture, will draw lines as human body, if set to false won't draw lines, default true.
        """
    def draw_seg_mask(self, img: maix._maix.image.Image, x: int, y: int, seg_mask: maix._maix.image.Image, threshold: int = 127) -> None:
        """
        Draw segmentation on image
        
        Args:
          - img: image object, maix.image.Image type.
          - seg_mask: segmentation mask image by detect method, a grayscale image
          - threshold: only mask's value > threshold will be draw on image, value from 0 to 255.
        """
    def input_format(self) -> maix._maix.image.Format:
        """
        Get input image format
        
        Returns: input image format, image::Format type.
        """
    def input_height(self) -> int:
        """
        Get model input height
        
        Returns: model input size of height
        """
    def input_size(self) -> maix._maix.image.Size:
        """
        Get model input size
        
        Returns: model input size
        """
    def input_width(self) -> int:
        """
        Get model input width
        
        Returns: model input size of width
        """
    def load(self, model: str) -> maix._maix.err.Err:
        """
        Load model from file
        
        Args:
          - model: Model path want to load
        
        
        Returns: err::Err
        """
