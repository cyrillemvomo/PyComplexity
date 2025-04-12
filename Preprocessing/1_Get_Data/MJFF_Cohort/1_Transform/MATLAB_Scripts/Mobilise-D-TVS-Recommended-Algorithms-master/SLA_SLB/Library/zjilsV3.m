
function sl_zjilstra_v3=zjilsV3(LB_vacc_high,fs,HSsamp,LBh)
%step length estimation using the biomechanical model propose by Zijlstra & Hof
%
% Zijlstra, W., & Hof, A. L. (2003). Assessment of spatio-temporal gait parameters from trunk accelerations during human walking.
% Gait & posture, 18(2), 1-10.
%
% Inputs:
%  - LB_vacc_high: vertical acceleration recorded on lower back, high-pass
%  filtered (here only the low pas filtered one as high pass filter is implemented)
%   - fs: sampling frequency of input data (acc signal)
%   - model: contains the correction factor 'K' estimated by data from NOT USED HERE
%   various clinical populations (training data)
%   - HSsamp: vector containing the timing of heal strikes (or initial contacts)
%   events (in samples)
%    - LBh: Low Back height, i.e., the distance from ground to sensor location on lower back (in cm) (HERE REPLACED BY ACTUAL HEIGHT IN m X 0.53)
%
% Output: 
%   - sl_zjilstra_v3: estimated step length
actual_LBh = (LBh*100)*0.53 %convert in cm and get actual_LBh

%%Convert and Pre_high-pass Filtering (Cyrille implementation of high pass filter as in the paper)
LB_vacc_high = LB_vacc_high/9.81
fc1=0.1;
[df1,cf1] = butter(4,fc1/(fs/2),'high');
vacc_high=filter(df1,cf1,LB_vacc_high);
%%%%% modif end
%vacc_high = LB_vacc_high
vspeed=-cumsum(vacc_high)./fs;

%drift removal (high pas filtering)
fc=1;
[df,cf] = butter(4,fc/(fs/2),'high');
speed_high=filter(df,cf,vspeed);

%estimate vertical displacement
vdis_high_v2=cumsum(speed_high)/fs;

h_jilstra_v3=zeros(length(HSsamp)-1,1);
for k=1:length(HSsamp)-1 % for each HS detected

    h_jilstra_v3(k)=abs(max(vdis_high_v2(HSsamp(k):HSsamp(k+1)))-min(vdis_high_v2(HSsamp(k):HSsamp(k+1))));

end

%K=model.zjilsV3.K;
% K=4.99;
%sl_zjilstra_v3=K*sqrt(abs((2*actual_LBh*h_jilstra_v3)-(h_jilstra_v3.^2))); %with correction factor try first
sl_zjilstra_v3=(2*sqrt(abs((2*actual_LBh*h_jilstra_v3)-(h_jilstra_v3.^2)))); % 2  √  2lh − h2 . without like paper

end