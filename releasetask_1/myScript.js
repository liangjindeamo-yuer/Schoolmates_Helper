//选择图片，马上预览

function xmTanUploadImg(obj) {
  var file = obj.files[0];
  //file.size 单位为byte  可以做上传大小控制
  console.log("file.size = " + file.size);

  var reader = new FileReader();
  //读取文件过程方法
  reader.onloadstart = function (e) {
    console.log("开始读取....");
  }

  reader.onprogress = function (e) {
    console.log("正在读取中....");
  }

  reader.onabort = function (e) {
    console.log("中断读取....");
  }

  reader.onerror = function (e) {
    console.log("读取异常....");
  }

  reader.onload = function (e) {
    console.log("成功读取....");
    var img = document.getElementById("xmTanImg");
    img.src = e.target.result;
    //或者 img.src = this.result;  //e.target == this
  }

  reader.readAsDataURL(file)
}

/* 添加标签 */

