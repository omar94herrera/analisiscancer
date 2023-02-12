function [x,y]=find_centroid(boundary)
    %object_index=unique(boundary(:,1));
    %n_objects=length(object_index);
    x=round(mean(boundary(:,1)));
    y=round((mean(boundary(:,2))+mean(boundary(:,3)))/2);
end