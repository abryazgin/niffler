#!/usr/bin/env php
<?php


# INIT
$uri = "testdir/2/somefile.txt";
$url = "http://office.rc-online.ru:22788/private/".$uri;
$headers = array("Authorization: e8738304de22ffdb812fc151c232af3ee5dd12b557f08d1f");
$headers2 = array("Authorization: 0b202c64e4ba86a0023a5b8a8a3e2a2b31578cc313340813");
$group_name = 'admin_client_group';

# PUT

$curl = curl_init($url);
$data = 'some wonderful string2';
print('UPLOADED CONTENT: '.$data."\n");
print("UPLOADING\n");
curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
curl_setopt($curl, CURLOPT_POSTFIELDS, $data);

$response = curl_exec($curl);
curl_close($curl);

# GET
$curl = curl_init();
print("DOWNLOADING BY OWNER\n");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data2 = curl_exec($curl);
print('DOWNLOADED CONTENT: '.$data2."\n");
curl_close($curl);

# GET 2
$curl = curl_init();
print("DOWNLOADING BY OTHER (ASSERT 403)\n");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers2);

$data2 = curl_exec($curl);
print('DOWNLOADED CONTENT BY OTHER: '.$data2."\n");
curl_close($curl);

# SHARE
$curl = curl_init();
print("SHARING TO GROUP\n");
$url_patch = $url.'?group='.$group_name;
curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PATCH");
curl_setopt($curl, CURLOPT_URL, $url_patch);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

curl_exec($curl);
curl_close($curl);

# GET 2
$curl = curl_init();
print("DOWNLOADING BY OTHER\n");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers2);

$data2 = curl_exec($curl);
print('DOWNLOADED CONTENT BY OTHER: '.$data2."\n");
curl_close($curl);

# DELETE
$curl = curl_init();
print("REMOVING\n");
curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "DELETE");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

curl_exec($curl);
curl_close($curl);

# GET
$curl = curl_init();
print("DOWNLOADING BY OWNER (ASSERT 403)\n");
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data2 = curl_exec($curl);
print('DOWNLOADED CONTENT: '.$data2."\n");
curl_close($curl);

?>
