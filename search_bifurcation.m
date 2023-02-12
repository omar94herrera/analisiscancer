function [b,y]=search_bifurcation(image,xinit,yinit,dir)
    b=false;
    y=[];
    [n_rows,n_col]=size(image);
    if xinit<1 || xinit>n_rows || yinit<1 || yinit>n_col
        return
    end
    if image(xinit,yinit)==0
        return
    end
    x=xinit+dir;
    if x<1 || x>n_rows
        return
    end
    [y_lower,y_upper]=search_limits(image,x,yinit);
    maxy=min([y_upper,n_col]);
    miny=max([y_lower,1]);
    if sum(image(x,miny:maxy))==0 || sum(image(x,miny:maxy))==maxy-miny+1
        return
    end
    b=true;
    while maxy>=miny
        if image(x,maxy)==1
            [y_lower,y_upper]=search_limits(image,x,maxy);
            y=[y,y_upper];
            maxy=y_lower;
        end
        maxy=maxy-1;
    end
end