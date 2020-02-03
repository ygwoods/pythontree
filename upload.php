<?php
if(isset($_FILES['a'])){
	if ($_FILES['a']['error']==0){
		copy($_FILES['a']['tmp_name'],"data");
	}
	else{echo "file error";}
}
else{echo "post error";}

?>
