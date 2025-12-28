
% 读取图片
 
 %img = imread('C:\Users\Administrator\Desktop\photo\1.bmp');  % 替换成你的图片路径

 img = imread('D:\单目结构光系统\data\threeshiftingpattern\3.bmp');  % 替换成你的图片路径
 
 %img = imread('D:\单目结构光系统\data\models\117\5\37.bmp');  % 替换成你的图片路径

 
% 转换为灰度图像
if size(img, 3) == 3
    % 如果是RGB彩色图像（3通道），使用rgb2gray转换
    gray_img = rgb2gray(img);
else
    % 如果已经是灰度图像（1通道），直接使用原图
    gray_img = img;
end

% 显示图片
imshow(img);

% 获取图片的尺寸
[rows, cols, channels] = size(img);

% 输出图片的像素值
disp('图片的像素值：');
disp(img);


