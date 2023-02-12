function [y_lower,y_upper]=search_limits(image,x,y)
    y_lower=y;
    y_upper=y;
    n_col=length(image(1,:));
    while image(x,y_upper)==1
        if y_upper==n_col
            break
        end
        y_upper=y_upper+1;
    end
    while image(x,y_lower)==1
        if y_lower==1
            break
        end
        y_lower=y_lower-1;
    end
end