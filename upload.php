<?php
#本文件需上传到Web服务器上,路径同tree.py中的url1。用于保存python的data数据
if(isset($_FILES['a'])){
	if ($_FILES['a']['error']==0){
		copy($_FILES['a']['tmp_name'],"data");
	}
	else{echo "file error";}
}
else{echo "post error";}

?>
