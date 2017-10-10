#!/usr/bin/env php
<?php


# INIT
$uri = "testdir/2/somefile.txt";
$url = "http://storage.rc-online.ru/private/".$uri;
$headers = array("Authorization: 8785ccfba9b838cbb2acd3694c5534c271737ee4");
$group_name = 'admin_client_group';

# GET
$curl = curl_init();
print("DOWNLOADING BY OWNER\n");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data = curl_exec($curl);
print('DOWNLOADED CONTENT: '.$data."\n");
curl_close($curl);
?>
