<?php

require_once 'rss-php/src/Feed.php';

$url=$argv[1];
$rss = Feed::loadRss($url);
$show=3600*24;

echo "Title: ", $rss->title;

foreach ($rss->item as $item) {
    $delta=time()-$item->timestamp;
    if ($delta<=$show) {
	$ts=$item->timestamp;
	$ts=date("d H:i",$delta);
	echo "-*NEXT*-", $item->title;
//	echo "\n", $item->link;
	echo "-*NEXT*-", $ts;
    }
}
