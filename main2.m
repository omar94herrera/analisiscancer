clc
clearvars
close all
tic
%% Variables to set by context
filename='003 Laminina (b).tif';
n_objects=20; %number of objects to identify and track
cut_confidence=0.85;    %Level of confidence cutting garbage data. It's recommended to set it around 0.9
loc_neighborhood=2;  %Radium of local filter
detection_confidence=0.9;  %Level of confidence detecting objects. It's recommended to set it around 0.9
r=100;  %Radium used to search chanels in the plate. It's recommended to be about 10% of the image's length
bl=5; %Magnitud of the image's blurring process
tol=4;

%% Reading files
info=imfinfo(filename);
n_frames=length(info);
for k=1:n_frames
    tiff(:,:,k)=imread(filename,k);
end
clear info

%% Cuting garbage data
[~,n_col]=size(tiff(:,:,1));
left_side=sum(tiff(:,1:15,1),'all');
right_side=sum(tiff(:,(n_col-14):n_col,1),'all');
if right_side<left_side
    for k=1:n_frames
        tiff(:,:,k)=imrotate(tiff(:,:,k),180);
    end
end
init_im=single(tiff(:,:,1));
[n_rows,n_col]=size(init_im);
m=sum(init_im,'all')/(n_rows*n_col);
s=sqrt(var(init_im,0,'all'));
low_threshold=norminv((1-cut_confidence)/2,m,s);
cut_index=0;
aux_im=init_im;
for i=1:length(init_im(:,1))
    current_index=0;
    while aux_im(i,current_index+1)<low_threshold
        cut_index=cut_index+1;
        current_index=current_index+1;
    end
    aux_im=aux_im(:,current_index+1:end);
end
tiff=tiff(:,cut_index+1:end,:);
clear init_im aux_im s m low_thres cut_index current_index

% name=split(filename,".");
% fmt=name(2);
% name=name(1);
% imwrite(tiff(:,:,1),name+"_cut"+"."+fmt);   %Crea un archivo con la imágen
% for i=2:n_frames
%     imwrite(tiff(:,:,i),name+"_cut"+"."+fmt,'WriteMode','append');  %Pega cada imágen a la anterior%
% end

%% Binarization
% [n_rows,n_col]=size(tiff(:,:,1));
% for k=1:n_frames
%     tiff(:,:,k)=logical(Filter(tiff(:,:,k)));
% end

%%Golbal Filter
init_im=single(tiff(:,:,1));
[n_rows,n_col]=size(init_im);
m=sum(init_im,'all')/(n_rows*n_col);
s=sqrt(var(init_im,0,'all'));
up_threshold=norminv((1+detection_confidence)/2,m,s);
tiff=tiff>up_threshold;
clear init_im s m up_threshold

% Detecting plate's chanels and more cuts
% aux_tiff=delete_dynamic(tiff,10);
% init_im=aux_tiff(:,:,1);

%% Cleaning set of images
% tiff=delete_static(tiff,bl,72);
% figure('Name','Clean')
% imshow(tiff(:,:,1));   %decomment to see the result :)

%% Detecting boundaries and Filling areas;
bound=[];
centroid=[];
aux_tiff=tiff;
%%Mejor rendimiento
for k=1:n_frames
    index=0;
    for i=n_rows:-1:1
        if index>n_objects
            break
        end
        for j=n_col:-1:1
            if index>=n_objects
                break
            end
            if aux_tiff(i,j,k)==1
                aux_bound=detect_boundary(tiff(:,:,k),i,j,-1,[]);
                aux_tiff(:,:,k)=delete_object(aux_tiff(:,:,k),aux_bound);
                if area(aux_bound)>tol
                    index=index+1;
                    lenbound=length(aux_bound(:,1));
                    bound=[bound;[index*ones(lenbound,1), aux_bound,k*ones(lenbound,1)]];
                    [centroid(index,2*k-1),centroid(index,2*k)]=find_centroid(aux_bound);
                end
            end
        end
    end
end
clear aux_tiff index aux_bound lenbound detect_boundary delete_object find_centroid
%%Útil si se quieren visualizar los resultados
% for k=1:n_frames
%     index=0;
%     for j=n_col:-1:1
%         for i=n_rows:-1:1
%             if tiff(i,j,k)==1
%                 aux_bound=detect_boundary(tiff(:,:,k),i,j,-1,[]);
%                 if area(aux_bound)<=tol
%                     tiff(:,:,k)=delete_object(tiff(:,:,k),aux_bound);
%                 else
%                     tiff(:,:,k)=fill_loc(tiff(:,:,k),aux_bound);
%                     if index<n_objects
%                         index=index+1;
%                         lenbound=length(aux_bound(:,1));
%                         bound(index,:,k)=[index*ones(lenbound,1), aux_bound];
%                         centroid(n_detected,k)=find_centroid(aux_bound);
%                     end
%                 end
%             end
%         end
%     end
% end
[centroid,bound]=reorganize(centroid,bound);
clear reorganize

%% Saving files
name=split(filename,".");
fmt=name(2);
name=name(1);
imwrite(tiff(:,:,1),name+"_binarized"+"."+fmt);   %Crea un archivo con la imágen
for i=2:n_frames
    imwrite(tiff(:,:,i),name+"_binarized"+"."+fmt,'WriteMode','append');  %Pega cada imágen a la anterior%
end
bound_name=name+"_boundaries.txt";
cent_name=name+"_centroids.txt";
writecell(num2cell(bound),bound_name);
writecell(num2cell(centroid),cent_name);
clearvars
toc