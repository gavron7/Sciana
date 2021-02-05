<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);



$api='';
$ow='https://api.openweathermap.org/data/2.5/weather?q=Lodz,Poland&lang=pl&units=metric&appid='.$api;
$dta=json_decode(file_get_contents($ow));

$w0['main']=(array) $dta->main;
$w0['akt']=(array) $dta->weather[0];
$w0['wind']=(array) $dta->wind;
$w0['vis']=(array) $dta->visibility;
$w0['ikona']="https://openweathermap.org/img/w/".$w0['akt']['icon'].".png";

$dev=null;
if (isset($_GET['dev'])) $dev=true;
if ($dev) {
    echo '<pre>';
    print_r($w0);
}

if (!$dev) header('Content-Type: image/png');
$png = imagecreatetruecolor(250, 80);
imagealphablending($png, false);
imagesavealpha($png, true);
$color = imagecolorallocatealpha($png, 0, 0, 0, 127); //127 means completely transparent.
$white = imagecolorallocate($png, 255, 255, 255);
$red = imagecolorallocate($png, 255, 0, 0);
$green = imagecolorallocate($png, 0, 255, 0);
$blue = imagecolorallocate($png, 0, 0, 255);
$black = imagecolorallocate($png, 0, 0, 0);

//imagefill($png, 0, 0, $color);

$text='DEMO';
//$font='fonts/Amatic-Bold.ttf';
$opis=$w0['main']['temp'];

function Wklej($co, $wco, $px=0, $py=0, $skala=1) {
    $png2 = imagecreatefrompng($co);
    imagealphablending($png2, false);
    imagesavealpha($png2, true);
    $sizex = imagesx($png2);
    $sizey = imagesy($png2);
    imagecopyresampled( $wco, $png2, $px, $py, 0, 0, $sizex, $sizey, $sizex, $sizey);
    return $wco;
}
function Wstaw($txt,$size,$font="RobotoCondensed-Light",$x,$y,$kolor,$obr) {
    imagettftext($obr, $size, 0, $x, $y, $kolor, "fonts/".$font.".ttf", $txt);
    return $obr;
}
$png=Wklej($w0['ikona'],$png,5,5);
$png=Wstaw($w0['akt']['description'],15,"RobotoCondensed-LightItalic",5,70,$white,$png);
$png=Wstaw(round($w0['main']['temp_min'])."&deg;C",15,"RobotoCondensed-Bold",60,55,$blue,$png);
$png=Wstaw(round($w0['main']['temp_max'])."&deg;C",15,"RobotoCondensed-Bold",60,20,$red,$png);
$png=Wstaw(round($w0['main']['temp'])."&deg;C",30,"RobotoCondensed-Bold",56,46,$black,$png);
$png=Wstaw(round($w0['main']['temp'])."&deg;C",30,"RobotoCondensed-Bold",55,45,$green,$png);
$png=Wstaw($w0['main']['pressure']."hPa",15,"Roboto-Thin",175,25,$white,$png);
$png=Wstaw($w0['main']['humidity']."%",15,"Roboto-Thin",200,50,$white,$png);

if (!$dev) imagepng($png);
imagedestroy($png);

