clear all;
close all;

dataset0 = csvread('data/patient4.csv',1,0);
dataset1 = csvread('data/patient3.csv',1,0);
%19,24
nattrib = size(dataset0,2);
attributes = [6,15,24,nattrib-2:nattrib-1];

%u0 = dataset0(1:end*3/4,attributes);
%y0 = dataset0(1:end*3/4,1);

%u1 = dataset0(end*3/4:end,attributes);
%y1 = dataset0(end*3/4:end,1);

u0 = [dataset0(:,attributes) ,[0; dataset0(1:end-1,1)]];
%u0 = [dataset0(1:end-1,1)];
y0 = dataset0(:,1);

u1 = [dataset1(:,attributes) ,[0; dataset1(1:end-1,1)]];
y1 = dataset1(:,1);

data0 = iddata(y0,u0,1);
data1 = iddata(y1,u1,1);

na=4;
nb = ones(1,size(u0,2))*5;
nc=4;
nk= ones(1,size(u0,2));

m1 = armax(data0,[na nb nc nk]);
%%
figure;
compare(m1,data0);
res = compare(m1,data0);
MSE = mse(res.y,y0)
benchMSE = mse(y0(2:end),y0(1:end-1))

%%
figure;
plot(y0(2:end))
hold on;
plot(y0(1:end-1))
title('Patient AS14.05');
xlabel('Time (days)')
ylabel('Normalized mood value');
legend('Estimation based on previous day','Current Mood value')
