function [sorted_cen,sorted_bound]=reorganize(centroids,bound)
    n_frames=length(centroids(1,:))/2;
    n_objects=length(centroids(:,1));
    aux_centroid(:,[1,2])=centroids(:,[1,2]);
    aux_bound=bound(bound(:,5)==1,:);
    for frame=2:n_frames
        lis=[];
        A=bound(bound(:,5)==frame,:);
        for object=1:n_objects
            ind=0;
            nearest=inf;
            for i=1:n_objects
                if (~ismember(i,lis)) && norm(centroids(object,[(2*(frame-1)-1),(2*(frame-1))])-centroids(i,[(2*frame-1),(2*frame)]))<nearest
                    ind=i;
                    nearest=norm(centroids(object,[2*(frame-1)-1,2*(frame-1)])-centroids(i,[2*(frame)-1,2*(frame)]));
                end
            end 
            lis=[lis, ind];
            aux_centroid(object,[2*frame-1,2*frame])=centroids(ind,[2*frame-1,2*frame]);
            lenbound=length(A(A(:,1)==ind,1));
            aux_bound=[aux_bound;[object*ones(lenbound,1),A(A(:,1)==ind,[2,3,4,5])]];
        end
    end
    sorted_cen=aux_centroid;
    sorted_bound=aux_bound;
end
%bound=[n_objeto,x_1,y1_inf,y1_sup]
%centroids=[[x1,y1,x2,y2,...]]