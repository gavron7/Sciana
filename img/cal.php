<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$ix=250;
$iy=250;

$png = imagecreatetruecolor($ix, $iy);

//imagealphablending($png, false);
//imagesavealpha($png, true);

$color = imagecolorallocatealpha($png, 0, 0, 0, 127); //127 means completely transparent.
$white = imagecolorallocate($png, 255, 255, 255);
$grey = imagecolorallocate($png, 64,64,64);
$dgrey = imagecolorallocate($png, 32, 32, 32);
$red = imagecolorallocate($png, 255, 0, 0);
$green = imagecolorallocate($png, 0, 255, 0);
$blue = imagecolorallocate($png, 0, 0, 255);
$black = imagecolorallocate($png, 0, 0, 0);

$miesiac=array('Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień');
$dzien=array('Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela');

$p='jesien';
if (date("m")<=9) $p='lato';
if (date("m")<=6) $p='wiosna';
if (date("m")<=3) $p='zima';


$png=Wklej("p_".$p.".png",$png,5,2,0.10);
$png=Wstaw($miesiac[date("m")-1],15,"RobotoCondensed-LightItalic",30,20,$white,$png);
$png=Wstaw(date("Y"),15,"RobotoCondensed-LightItalic",$ix-50,20,$white,$png);
//imagerectangle($png, 5,30, $ix-5, $iy-5, $white);
$iloscdni=date("t");
$pierwszy=date('N',mktime(1,1,1,date("m"),1,date("Y")));
$ost=date('t', strtotime("-1 MONTH"));

$dx=($ix-10)/7;
$dy=($iy-35)/(31/5);
$syy=40;
$sxx=5;
$xx=$sxx;
$yy=$syy;

$swieto='  ';
$a=0; if (isset($_GET['a'])) $a=1;
if ($a==1)
    echo $pierwszy;
// opisy
for ($i=0; $i<7; $i++) {
//    imagerectangle($png, 5,30, $ix-5, $iy-5, $white);
    $png=Wstaw(substr($dzien[$i+1],0,3),8,"RobotoCondensed-LightItalic",7+$xx,$yy,$grey,$png);
    $xx=$xx+$dx;
}


for ($i=0; $i<$pierwszy; $i++)
    $td[]=($ost-$pierwszy+$i+1).' ';
for ($i=1; $i<=$iloscdni; $i++)
    $td[]=$i;
for ($i=1; $i<30; $i++)
    $td[]=$i." ";

$dzis=date("d");

$xx=$sxx; $yy=$yy+$dy;
// kalendarz
for ($d=1; $d<=$iloscdni; $d=$d+7) {
    for ($i=0; $i<7; $i++) {
        if (date("d")==$td[$d+$i]) {
            imagefilledrectangle($png,$xx,$yy,$xx+$dx,$yy-$dy,$white);
            $k=$black;
            if (CzySwieto($td[$d+$i])) $k=$red;
            $png=Wstaw($td[$d+$i],15,"RobotoCondensed-LightItalic",$xx,$yy-10,$k,$png);
        } else {
            imagerectangle($png,$xx,$yy,$xx+$dx,$yy-$dy,$dgrey);
            $k=$white; 
            if (CzySwieto($td[$d+$i])) $k=$red;
            if (trim($td[$d+$i])!=$td[$d+$i]) {
                $k=$dgrey; 
            }
            $png=Wstaw($td[$d+$i],10,"RobotoCondensed-LightItalic",$xx,$yy,$k,$png);

        }
        $xx=$xx+$dx;
    }
    $xx=$sxx;
    $yy=$yy+$dy;
}
function CzySwieto($dzien) {
    global $swieto;
    if (trim($dzien)==$dzien) 
        if (strpos("!!!!".$swieto,date('Y-m-'.$dzien)))
            return true;
}
if ($a==0) {
header('Content-Type: image/png');
imagejpeg($png);
imagedestroy($png);
}

function Wklej($co, $wco, $px=0, $py=0, $skala=1) {
    $png2 = imagecreatefrompng($co);
    imagealphablending($png2, false);
    imagesavealpha($png2, true);
    $sizex = imagesx($png2);
    $sizey = imagesy($png2);
    imagecopyresampled( $wco, $png2, $px, $py, 0, 0, $sizex*$skala, $sizey*$skala, $sizex, $sizey);
    return $wco;
}

function Wstaw($txt,$size,$font="RobotoCondensed-Light",$x,$y,$kolor,$obr) {
    imagettftext($obr, $size, 0, $x, $y, $kolor, "fonts/".$font.".ttf", $txt);
    return $obr;
}
