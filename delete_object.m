function deleted=delete_object(image,boundary)
    if isempty(boundary)
        deleted=image;
        return
    end
    for i=1:length(boundary(:,1))
        b=boundary(i,:);
        x=b(1); y_lower=b(2); y_upper=b(3);
        image(x,y_lower:y_upper)=0;
    end
    deleted=image;
end