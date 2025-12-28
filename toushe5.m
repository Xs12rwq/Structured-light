
load("xtie_p.mat");
load("ytie_p.mat");

load("graytie6.mat");
imgpro_255=zeros(800,1280);
% img255=ones(800,1280).*255;
% mask=ones(800,1280);



img_1=imread("D:\单目结构光系统\data1\models\9009\1.bmp");
img_1=rgb2gray(img_1);
img_1=double(img_1);
[a1,a2]=find(img_1>250);
L=length(a1);


for i=1:L
    disp(i);
    %xx1 = max(1, min(1280, floor(x_p(a1(i), a2(i)))));
    %xx2 = max(1, min(1280, ceil(x_p(a1(i), a2(i)))));
    %yy1 = max(1, min(800,  floor(y_p(a1(i), a2(i)))));
    %yy2 = max(1, min(800,  ceil(y_p(a1(i), a2(i)))));

    xx1=floor(x_p(a1(i),a2(i))+1);   
    xx2=ceil(x_p(a1(i),a2(i))+1);
    yy1=floor(y_p(a1(i),a2(i))+1);
    yy2=ceil(y_p(a1(i),a2(i))+1);

    if imgpro_255(yy1,xx1)==0
        imgpro_255(yy1,xx1)=gray(i);
    end
    if imgpro_255(yy1,xx2)==0
        imgpro_255(yy1,xx2)=gray(i);
    end
    
    if imgpro_255(yy2,xx1)==0
        imgpro_255(yy2,xx1)=gray(i);
    end
    
    if imgpro_255(yy2,xx2)==0
        imgpro_255(yy2,xx2)=gray(i);
    end    
      
    if imgpro_255(yy1,xx1)>0
        if imgpro_255(yy1,xx1)>gray(i)
            imgpro_255(yy1,xx1)=gray(i);
        end
    end  
    if imgpro_255(yy1,xx2)>0
        if imgpro_255(yy1,xx2)>gray(i)
            imgpro_255(yy1,xx2)=gray(i);
        end
    end   
    if imgpro_255(yy2,xx1)>0
        if imgpro_255(yy2,xx1)>gray(i)
            imgpro_255(yy2,xx1)=gray(i);
        end
    end  
    
    
    if imgpro_255(yy2,xx2)>0
        if imgpro_255(yy2,xx2)>gray(i)
            imgpro_255(yy2,xx2)=gray(i);
        end
    end      
        

end

[f1,f2]=find(imgpro_255==0);
L_f=length(f1);
for m=1:L_f
    imgpro_255(f1(m),f2(m))=255;
end


imgpro_255=uint8(imgpro_255);

imwrite(imgpro_255,"D:\单目结构光系统\data1\tie_zuijia6.bmp");


W = 1280;
H = 800;
A = 0.5;
B = 0.5;
N = 12;

n = 4;
T_X = W / (2 ^ n);
T_Y = H / (2 ^ n);


[~, patterns_phaseshift_X] = m_make_phase_shift_patterns(A, B, N, W, H,imgpro_255);



save_folder="D:\单目结构光系统\data1\tie_zuijia6";



for i = 1: N
    save_file_img = strcat(save_folder, "/", int2str(i), ".bmp"); 
    disp("写入文件到:" + save_file_img);
    img = squeeze(patterns_phaseshift_X(:,:,i));
    img=uint8(img);
    imwrite(img, save_file_img);   %两个参数 一个是文件 另一个是文件名
end

function [Is, Is_img] = m_make_phase_shift_patterns(A, B, N, W, H, imgpro_255)
    Is = cell(N, 1);
    Is_img = zeros(H, W, N);
    for k = 0:N-1
        for w = 1:W
            for h = 1:H
                % h从1~H，周期数N
                % 2π*N*(h-1)/H 让整个图像有N个条纹周期
                I = double(imgpro_255(h, w)) * (A + B * cos(2 * pi * 16 * (h-1) / H - 2 * pi * k / N));
                Is_img(h, w, k+1) = floor(I);
            end
        end
    end
end










