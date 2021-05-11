insert into clientlist(clientname,clientpassword) values("test","test");#add client 
select clientname,clientid from clientlist; #see all created users

select clientpassword from clientlist where clientname="test"; #select existing user for password control

select clientname from activeclients;#see all active users

insert into activeclients(clientname) values("marijn"); #new online user 

delete from activeclients where clientname="marijn";#user has disconnected