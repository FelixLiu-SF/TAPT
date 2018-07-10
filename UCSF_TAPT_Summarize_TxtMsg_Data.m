
% read in enrollment data
tapt_sms_enrollment_f = 'C:\Users\fliu2\Box Sync\UCSF_TAPT_Share\Participant_Cells.xlsx';

[~,~,x_raw_enrolled] = xlsread(tapt_sms_enrollment_f);

% santize enrollment data

f_enroll = indcfind(x_raw_enrolled(1,:),'^Enrolled$','regexpi');
f_cellphone = indcfind(x_raw_enrolled(1,:),'^CellPhone$','regexpi');
f_baseline = indcfind(x_raw_enrolled(1,:),'^BaselineDate$','regexpi');
f_StudyID = indcfind(x_raw_enrolled(1,:),'^Study ID$','regexpi');

x_raw_enrolled(:,f_StudyID) = cellfun(@num2str,x_raw_enrolled(:,f_StudyID),'UniformOutput',0);
x_raw_enrolled = x_raw_enrolled(indcfind(x_raw_enrolled(:,f_StudyID),'~','nan'),:);
x_raw_enrolled(:,f_enroll) = cellfun(@num2str,x_raw_enrolled(:,f_enroll),'UniformOutput',0);

x_enrolled = x_raw_enrolled(indcfind(x_raw_enrolled(:,f_enroll),'1','regexpi'),:);
for ix=1:size(x_enrolled,1)

  tmp_cellphone = x_enrolled{ix,f_cellphone};
  tmp_cellphone = strrep(tmp_cellphone,'-','');
  tmp_cellphone = horzcat('1',tmp_cellphone);

  x_enrolled{ix,f_cellphone} = tmp_cellphone;

  tmp_BLdate = x_enrolled{ix,f_baseline};
  tmp_BLdate = datenum(tmp_BLdate,'mm/dd/yyyy');

  x_enrolled{ix,f_baseline} = tmp_BLdate;

end

% read in raw txt msg data
% tapt_sms_raw_data_f = 'C:\Users\fliu2\Box Sync\UCSF_TAPT_Share\UCSF_TAPT_ReceivedMessages.csv';
tapt_sms_raw_data_f = 'UCSF_TAPT_ReceivedMessages_20180710_processed.csv';

[~,~,x_raw_data] = xlsread(tapt_sms_raw_data_f);

% convert date/time and change to pacific time but remember daylight savings time
spring_foward_utc = datenum(2018,3,11,10,0,0);
f_datetime = indcfind(x_raw_data(1,:),'^DateTime$','regexpi');
x_pst_data = x_raw_data;
for ix = 2:size(x_raw_data,1)

  tmp_raw_dt = x_raw_data{ix,f_datetime};
  tmp_matlab_dt = datenum(tmp_raw_dt,'yyyy-mm-dd HH:MM:SS');
  
  if(tmp_matlab_dt<spring_foward_utc)
      tmp_matlab_dt_pst = tmp_matlab_dt-datenum(0,0,0,8,0,0);
  else
      tmp_matlab_dt_pst = tmp_matlab_dt-datenum(0,0,0,7,0,0);
  end

  x_pst_data{ix,f_datetime} = tmp_matlab_dt_pst;

end

% filter for enrolled phone numbers only
f_fromnumber = indcfind(x_raw_data(1,:),'^From$','regexpi');
x_pst_data(:,f_fromnumber) = cellfun(@num2str,x_pst_data(:,f_fromnumber),'UniformOutput',0);

x_pst_data = x_pst_data(ismember(x_pst_data(:,f_fromnumber),x_enrolled(:,f_cellphone)),:);

% filter for valid responses only
f_body = indcfind(x_raw_data(1,:),'^Body$','regexpi');
x_pst_data(:,f_body) = cellfun(@num2str,x_pst_data(:,f_body),'UniformOutput',0);
x_pst_data(:,f_body) = cellfun(@strtrim,x_pst_data(:,f_body),'UniformOutput',0);

x_pst_data_01 = x_pst_data(indcfind(x_pst_data(:,f_body),'^(0|1)$','regexpi'),:);

% look up unique "from" phone numbers
unique_fromnumbers = unique(x_pst_data_01(:,f_fromnumber));

% look up metadata from enrollment
for ix=1:size(unique_fromnumbers,1)
   
    tmp_fromnumber = unique_fromnumbers{ix,1};
    jx = indcfind(x_enrolled(:,f_cellphone),tmp_fromnumber,'regexpi');
    
    tmp_BLdate = x_enrolled{jx(1),f_baseline};
    unique_fromnumbers{ix,2} = tmp_BLdate; 
    
    tmp_StudyID = x_enrolled{jx(1),f_StudyID};
    unique_fromnumbers{ix,3} = tmp_StudyID; 
    
end

% collect unique answers by day
x_pst_data_01_byday = {};
f_fromID = f_fromnumber;

for ix=1:size(unique_fromnumbers,1)

    tmp_fromnumber = unique_fromnumbers{ix,1};
    tmp_BLdate = unique_fromnumbers{ix,2};
    tmp_StudyID = unique_fromnumbers{ix,3};
    
    tmp_chunk = x_pst_data_01(indcfind(x_pst_data_01(:,f_fromnumber),tmp_fromnumber,'regexpi'),:);
    
    % relabel with StudyID
    tmp_chunk(:,f_fromnumber) = strrep(tmp_chunk(:,f_fromnumber),tmp_fromnumber,tmp_StudyID);
    
    % get date/times
    tmp_chunk_dt = cell2mat(tmp_chunk(:,f_datetime));
    
    for jx=1:42
        
        tmp_day = tmp_BLdate + jx;
        
        kx = find(tmp_chunk_dt>=tmp_day & tmp_chunk_dt<(tmp_day+1));
        
        tmp_new_row = {};
        
        % collect only 1 record per day
        if(isempty(kx))
            % no response this day
            tmp_new_row = {};
            
        elseif(size(kx,1)==1)
            % use this record
            tmp_new_row = tmp_chunk(kx(1),:);
            
        elseif(size(kx,1)>1)
            % multiple responses
            
            tmp_unique_body = unique(tmp_chunk(kx,f_body));
            if(size(tmp_unique_body,1)==1)
                % responses for the day are consistent, use 1st response
                tmp_new_row = tmp_chunk(kx(1),:);
                
            else
                % non-unique responses for the day
                
                % try to choose only responses close to 8 pm
                lx = find(tmp_chunk_dt>=(tmp_day+datenum(0,0,0,8,0,0)) & tmp_chunk_dt<(tmp_day+1));
                
                if(size(lx,1)==1)
                    % only 1 response around 8 pm, use this record
                    tmp_new_row = tmp_chunk(lx(1),:);
                    
                else
                    % if that doesn't work, choose the latest response
                    tmp_new_row = tmp_chunk(lx(1),:);
                    
                end
                
            end
        end
        
        if(~isempty(tmp_new_row))
            
            tmp_PSTstr = datestr(tmp_new_row{1,f_datetime},'yyyymmdd HH:MM:SS');
            tmp_BLstr = datestr(tmp_BLdate,'yyyymmdd');
            
            tmp_new_row = [tmp_new_row, tmp_PSTstr, tmp_BLstr, jx, ceil(jx/7)];
            
            x_pst_data_01_byday = [x_pst_data_01_byday; tmp_new_row];
        end
        
    end
    
end

f_PSTstr = size(x_pst_data_01_byday,2)-3;
f_BLstr = size(x_pst_data_01_byday,2)-2;
f_daynum = size(x_pst_data_01_byday,2)-1;
f_weeknum = size(x_pst_data_01_byday,2);

x_byday = x_pst_data_01_byday(:,[f_fromID, f_BLstr, f_PSTstr, f_daynum, f_weeknum, f_body]);
h_byday = {'StudyID', 'EnrollmentDate', 'ResponseDateTime', 'ResponseDayNumber', 'ResponseWeekNumber', 'ResponseMessage'};

% summarize over whole study
x_summary_study = {};
h_summary_study = {'StudyID', 'NumberResponses_0', 'NumberResponses_1', 'NumberResponses_Total', 'PercentageTotalPossible_0', 'PercentageTotalPossible_1', 'PercentageTotal_1'};
for ix=1:size(unique_fromnumbers,1)

  tmp_StudyID = unique_fromnumbers{ix,3};
  
  tmp_chunk = x_pst_data_01_byday(indcfind(x_pst_data_01_byday(:,f_fromID),tmp_StudyID,'regexpi'),:);

  tmp_0 = size(indcfind(tmp_chunk(:,f_body),'^0$','regexpi'),1);
  tmp_1 = size(indcfind(tmp_chunk(:,f_body),'^1$','regexpi'),1);

  x_summary_study{ix,1} = tmp_StudyID;
  x_summary_study{ix,2} = tmp_0;
  x_summary_study{ix,3} = tmp_1;
  x_summary_study{ix,4} = (tmp_0+tmp_1);
  x_summary_study{ix,5} = (tmp_0/(42))*100;
  x_summary_study{ix,6} = (tmp_1/(42))*100;
  
  if((tmp_0+tmp_1)>0)
      x_summary_study{ix,7} = (tmp_1/(tmp_0+tmp_1))*100;
  else
      x_summary_study{ix,7} = 0;
  end

end

% summarize week by week
x_summary_week = {};
h_summary_week = {'StudyID', 'NumberResponsesWk_0', 'NumberResponsesWk_1', 'NumberResponsesWk_Total', 'PercentageTotalPossibleWk_0', 'PercentageTotalPossibleWk_1', 'PercentageTotalWk_1', 'ResponseWeekNumber'};
index = 0;

for ix=1:size(unique_fromnumbers,1)


  tmp_StudyID = unique_fromnumbers{ix,3};
  tmp_BLdate = unique_fromnumbers{ix,2};
  
  tmp_chunk = x_pst_data_01_byday(indcfind(x_pst_data_01_byday(:,f_fromID),tmp_StudyID,'regexpi'),:);
  tmp_chunk = sortrows(tmp_chunk,f_datetime);
  tmp_chunk_dt = cell2mat(tmp_chunk(:,f_datetime));
  
  for jx=1:6
      
        index = index+1;
        
        tmp_wk_start = (tmp_BLdate+1) + (jx-1)*7;
        tmp_wk_stop = (tmp_BLdate+1) + (jx)*7;
        
        kx = find(tmp_chunk_dt>=tmp_wk_start & tmp_chunk_dt<tmp_wk_stop);
        
        tmp_chunk_wk = tmp_chunk(kx,:);
        
        tmp_0 = size(indcfind(tmp_chunk_wk(:,f_body),'^0$','regexpi'),1);
        tmp_1 = size(indcfind(tmp_chunk_wk(:,f_body),'^1$','regexpi'),1);
        
        x_summary_week{index,1} = tmp_StudyID;
        x_summary_week{index,2} = tmp_0;
        x_summary_week{index,3} = tmp_1;
        x_summary_week{index,4} = (tmp_0+tmp_1);
        x_summary_week{index,5} = (tmp_0/(7))*100;
        x_summary_week{index,6} = (tmp_1/(7))*100;
        x_summary_week{index,8} = jx;

        if((tmp_0+tmp_1)>0)
          x_summary_week{index,7} = (tmp_1/(tmp_0+tmp_1))*100;
        else
          x_summary_week{index,7} = 0;
        end
        
  end
  
end


% output csv files

summary_study_outf = horzcat('TAPT_Response_Summary_Study_',datestr(now,'yyyymmdd'),'.csv');
summary_week_outf = horzcat('TAPT_Response_Summary_Week_',datestr(now,'yyyymmdd'),'.csv');
data_byday_outf = horzcat('TAPT_Response_CleanData_ByDay_',datestr(now,'yyyymmdd'),'.csv');

dlmtxtwrite([h_summary_study; x_summary_study],summary_study_outf,',','cell','',1);
dlmtxtwrite([h_summary_week; x_summary_week],summary_week_outf,',','cell','',1);
dlmtxtwrite([h_byday; x_byday],data_byday_outf,',','cell','',1);


