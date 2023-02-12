function ar=area(bound)
    ar=sum(bound(:,3))-sum(bound(:,2))+length(bound(:,1));
end