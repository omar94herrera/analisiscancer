function bound=detect_boundary(image,xinit,yinit,dir,boundary)
%función recursiva
    %image: image where is the object's boundary to search
    %[prev_x,prev_y]: vector of previous initial points
    %[init_x,init_y]: pixel where the search is started
    %object_index: object's ID
    %first_rec: boolean value that indicates if this is the first recurtion
    [n_rows,n_col]=size(image);
    bound=boundary;
    if xinit<1 || xinit>n_rows || yinit<1 || yinit>n_col
        return
    end
    if image(xinit,yinit)==0
        return
    end
    [y_lower,y_upper]=search_limits(image,xinit,yinit);
    if ismember([xinit,y_lower,y_upper],bound)
        return
    end
    if xinit+dir<1 || xinit+dir>n_rows
        return
    end
    maxy=min([y_upper+1,n_col]);
    miny=max([y_lower-1,1]);
    bound=[bound;[xinit,y_lower,y_upper]];
    while sum(image(xinit+dir,miny:maxy))>0
        [b2,ydir2]=search_bifurcation(image,xinit,y_upper,-dir);
        %% Solo evalua los extremos de y, ojo con eso, si se evaluan todos, queda como lo comentado
        if b2
            for i=1:length(ydir2)
                [ydir_low,ydir_up]=search_limits(image,xinit-dir,ydir2(i));
                if ~ismember([xinit-dir,ydir_low,ydir_up],bound)
                    bound=[bound;detect_boundary(image,xinit-dir,ydir_up,-dir,bound)];
                end
            end
        end
%         if b2
%             [ydir_low1,ydir_up1]=search_limits(image,xinit-dir,ydir2(1));
%             [ydir_low2,ydir_up2]=search_limits(image,xinit-dir,ydir2(end));
%             if ~ismember([xinit-dir,ydir_low1,ydir_up1],bound)
%                 bound=[bound;detect_boundary(image,xinit-dir,ydir_up1,-dir,bound)];
%             end
%             if ~ismember([xinit-dir,ydir_low2,ydir_up2],bound)
%                 bound=[bound;detect_boundary(image,xinit-dir,ydir_up2,-dir,bound)];
%             end
%         end
        [b1,ydir1]=search_bifurcation(image,xinit,y_upper,dir);
        %% Solo evalua los extremos de y, ojo con eso, si se evaluan todos, queda como lo comentado
        if b1
            for i=1:length(ydir1)
                [ydir_low,ydir_up]=search_limits(image,xinit+dir,ydir1(i));
                if ~ismember([xinit+dir,ydir_low,ydir_up],bound)
                    bound=[bound;detect_boundary(image,xinit+dir,ydir_up,dir,bound)];
                end
            end
        end
%         if b1
%             [ydir_low1,ydir_up1]=search_limits(image,xinit+dir,ydir1(1));
%             [ydir_low2,ydir_up2]=search_limits(image,xinit+dir,ydir1(end));
%             if ~ismember([xinit+dir,ydir_low1,ydir_up1],bound)
%                 
%                 bound=[bound;detect_boundary(image,xinit+dir,ydir_up1,dir,bound)];
%             end
%             if ~ismember([xinit+dir,ydir_low2,ydir_up2],bound)
%                 bound=[bound;detect_boundary(image,xinit+dir,ydir_up2,dir,bound)];
%             end
%         end
        xinit=xinit+dir;
        ind=find(image(xinit,miny:maxy));
        yinit=miny+ind(1)-1;
        [y_lower,y_upper]=search_limits(image,xinit,yinit);
        maxy=min([y_upper+1,n_col]);
        miny=max([y_lower-1,1]);
        if ~b1 && (xinit+dir<1 || xinit+dir>n_rows)
            bound=[bound;[xinit,y_lower,y_upper]];
            break
        else
            if ~b1
                bound=[bound;[xinit,y_lower,y_upper]];
            end
        end
    end
    indx=unique(bound(:,1));
    lenx=length(indx);
    aux_bound=bound;
    bound=[];
    for i=1:lenx
        indy=aux_bound(aux_bound(:,1)==indx(i),:);
        y_lower=min(indy(:,2));
        y_upper=max(indy(:,3));
        bound(i,:)=[indx(i),y_lower,y_upper];
    end
    
end