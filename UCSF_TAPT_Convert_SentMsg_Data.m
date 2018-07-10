% read in raw sent txt msg data

tapt_sms_raw_data_f = 'UCSF_TAPT_SentMessages_20180710.csv';

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

% delete new line chars
for ix = 2:size(x_pst_data,1)
    
    tmp_body = x_pst_data{ix,6};
    tmp_body(tmp_body==sprintf('\n')) = ' ';
    
    x_pst_data{ix,6} = tmp_body;
    
end


data_pst_outf = horzcat('TAPT_TextMsg_Sent_CleanData_',datestr(now,'yyyymmdd'),'.xlsx');

xlswrite(data_pst_outf,x_pst_data);

% dlmtxtwrite([x_pst_data],data_pst_outf,',','cell','',1);