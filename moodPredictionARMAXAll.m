clear all;
close all;
%%
files = dir('data');
fc = size(files,1)-3;

MSEs = zeros(1,fc);
for i=0:fc
    filename = sprintf('data/patient%d.csv',i);
    dataset0 = csvread(filename,1,0);

    if i==1 || i==11 || i==14 || i==20
        continue;
    end
    
    nattrib = size(dataset0,2);
    attributes = [6,15,24,nattrib-2:nattrib-1];


    u0 = dataset0(:,attributes);
    y0 = dataset0(:,1);
    data0 = iddata(y0,u0,1);

    na=4;
    nb = ones(1,size(u0,2))*5;
    nc=4;
    nk= ones(1,size(u0,2));

    m1 = armax(data0,[na nb nc nk]);
    %%
    res = compare(m1,data0);
    MSE = mse(res.y,y0);
    MSEs(i+1)=MSE;
end

MSEs(m>10 | m==0)=inf;
scatter(1:fc+1,MSEs);
title('MSE of Subjects');
xlabel('Subject');
ylabel('MSE on normalized dataset')
%compare(m1,data0);