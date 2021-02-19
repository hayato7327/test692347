window.alert("1行目")
$(".like-btn").click(function(e){
  window.alert("1")
  e.preventDefault()
  window.alert("2")
  const this_ = $(this);
  window.alert("3")
  const like_cnt = $(".liked-cnt");
  window.alert(like_cnt)
  const likeUrl = this_.attr("data-href");
  window.alert(likeUrl)
  if (likeUrl){
    window.alert("prepare ajax")
    $.ajax({
      url: likeUrl,
      method: "GET",
      data: {"status":1}, //　いいねが押されましたと伝える
    })
    .then(
      function(data){
        window.alert("success")
        let change_like = like_cnt.text();
        if (data.liked){　//　もしいいねされていなかったら
          like_cnt.text(++change_like);　//　いいねの数を１追加
          this_.addClass("on");　//　ボタンをピンクに
        } else {　　//　もしいいねされていたら
          like_cnt.text(--change_like);　//　いいねの数を１減らす
          this_.removeClass("on");　//　ボタンのデザインを初期状態に
        }
      },
      function(error){
        console.log("error")
      }
    )
  } else {
    window.alert("else")
  }
})
