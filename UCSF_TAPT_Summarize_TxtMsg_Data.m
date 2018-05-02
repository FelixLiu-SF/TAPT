
% read in raw txt msg data
tapt_sms_raw_data_f = 'UCSF_TAPT_ReceivedMessages.csv';

[~,~,x_raw_data] = xlsread(tapt_sms_raw_data_f);

% convert date/time and change to pacific time
x_pst_data = x_raw_data;
for ix = 2:size(x_raw_data,1)

  tmp_raw_dt = x_raw_data{ix,2};
  tmp_matlab_dt = datenum(tmp_raw_dt,'yyyy-mm-dd HH:MM:SS');
  tmp_matlab_dt_pst = tmp_matlab_dt-datenum(0,0,0,8,0,0);

  x_pst_data{ix,2} = tmp_matlab_dt_pst;

end

% filter for valid responses only
f_body = indcfind(x_pst_data(1,:),'^Body$','regexpi');
x_pst_data(:,f_body) = cellfun(@num2str,x_pst_data(:,f_body),'UniformOutput',0);
x_pst_data(:,f_body) = cellfun(@strtrim,x_pst_data(:,f_body),'UniformOutput',0);

x_pst_data_01 = x_pst_data(indcfind(x_pst_data(:,f_body),'^(0|1)$','regexpi'),:);

% look up unique "from" phone numbers
f_fromnumber = indcfind(x_pst_data_01(1,:),'^From$','regexpi');
x_pst_data_01(:,f_fromnumber) = cellfun(@num2str,x_pst_data_01(:,f_fromnumber),'UniformOutput',0);

unique_fromnumbers = unique(x_pst_data_01(:,f_fromnumber));

% look up metadata from enrollment 

% summarize over whole study
x_summary_study = {};
h_summary_study = {'From', 'NumberResponses_0', 'NumberResponses_1'};
for ix=1:size(unique_fromnumbers,1)

  tmp_fromnum = unique_fromnumbers{ix,1};
  jx = indcfind(x_pst_data_01(:,f_fromnumber),tmp_fromnum,'regexpi');

  tmp_chunk = x_pst_data_01(jx,:);

  tmp_0 = size(indcfind(tmp_chunk(:,f_body),'^0$','regexpi'));
  tmp_1 = size(indcfind(tmp_chunk(:,f_body),'^1$','regexpi'));

  x_summary_study{ix,1} = tmp_fromnum;
  x_summary_study{ix,2} = tmp_0;
  x_summary_study{ix,3} = tmp_1;
  x_summary_study{ix,4} = (tmp_0/(42))*100;
  x_summary_study{ix,5} = (tmp_1/(42))*100;
  x_summary_study{ix,6} = (tmp_1/(tmp_0+tmp_1))*100;

end

% summarize week by week
