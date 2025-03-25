document.getElementById("deletePostConfirm").onclick = function() {
    let deleteConfirm = confirm('投稿を削除してよろしいですか？');
    
    if(deleteConfirm) {
      document.getElementById("deletePostConfirm").submit();
    } else {
      alert("削除をキャンセルしました。")
    }
  };