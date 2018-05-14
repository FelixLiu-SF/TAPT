
% read in enrollment data
tapt_sms_enrollment_f = 'C:\Users\fliu2\Box Sync\UCSF_TAPT_Share\Participant_Cells.xlsx';

[~,~,x_raw_enrolled] = xlsread(tapt_sms_enrollment_f);

% santize enrollment data

f_enroll = indcfind(x_raw_enrolled(1,:),'^Enrolled$','regexpi');
f_cellphone = indcfind(x_raw_enrolled(1,:),'^CellPhone$','regexpi');
f_baseline = indcfind(x_raw_enrolled(1,:),'^BaselineDate$','regexpi');

x_raw_enrolled = x_raw_enrolled(indcfind(x_raw_enrolled(:,indcfind(x_raw_enrolled(1,:),'^Study ID$','regexpi')),'~','nan'),:);
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
tapt_sms_raw_data_f = 'C:\Users\fliu2\Box Sync\UCSF_TAPT_Share\UCSF_TAPT_ReceivedMessages.csv';

[~,~,x_raw_data] = xlsread(tapt_sms_raw_data_f);

% convert date/time and change to pacific time
f_datetime = indcfind(x_raw_data(1,:),'^DateTime$','regexpi');
x_pst_data = x_raw_data;
for ix = 2:size(x_raw_data,1)

  tmp_raw_dt = x_raw_data{ix,f_datetime};
  tmp_matlab_dt = datenum(tmp_raw_dt,'yyyy-mm-dd HH:MM:SS');
  tmp_matlab_dt_pst = tmp_matlab_dt-datenum(0,0,0,8,0,0);

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

% summarize over whole study
x_summary_study = {};
h_summary_study = {'From', 'NumberResponses_0', 'NumberResponses_1'};
for ix=1:size(unique_fromnumbers,1)

  tmp_fromnum = unique_fromnumbers{ix,1};
  jx = indcfind(x_pst_data_01(:,f_fromnumber),tmp_fromnum,'regexpi');

  tmp_chunk = x_pst_data_01(jx,:);

  tmp_0 = size(indcfind(tmp_chunk(:,f_body),'^0$','regexpi'),1);
  tmp_1 = size(indcfind(tmp_chunk(:,f_body),'^1$','regexpi'),1);

  x_summary_study{ix,1} = tmp_fromnum;
  x_summary_study{ix,2} = tmp_0;
  x_summary_study{ix,3} = tmp_1;
  x_summary_study{ix,4} = (tmp_0/(42))*100;
  x_summary_study{ix,5} = (tmp_1/(42))*100;
  x_summary_study{ix,6} = (tmp_1/(tmp_0+tmp_1))*100;

end

% summarize week by week
