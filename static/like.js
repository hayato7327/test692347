$(function(){
  const this_ = $(".like-btn");
  const likeUrl = this_.attr("data-href"); // ユーザーのステータス情報
  $.ajax({
    url: likeUrl,
    method: "GET",
    data: {"status":0},　// ユーザーのステータス情報を変更しないように
    success: function(data){
      if (data.liked){　// もしユーザーが既にいいねをしていた場合
          this_.addClass("on");　// ボタンをピンクにする
      }
    }, error: function(error){
      console.log("error")
    }
  })
});

$(".like-btn").click(function(e){
  e.preventDefault()
  const this_ = $(this);
  const like_cnt = $(".liked-cnt");
  const likeUrl = this_.attr("data-href");
  if (likeUrl){
      $.ajax({
      url: likeUrl,
      method: "GET",
      data: {"status":1}, //　いいねが押されましたと伝える
      success: function(data){
        let change_like = like_cnt.text();
        if (data.liked){　//　もしいいねされていなかったら
          like_cnt.text(++change_like);　//　いいねの数を１追加
          this_.addClass("on");　//　ボタンをピンクに
        } else {　　//　もしいいねされていたら
          like_cnt.text(--change_like);　//　いいねの数を１減らす
          this_.removeClass("on");　//　ボタンのデザインを初期状態に
        }
      }, error: function(error){
        console.log("error")
      }
    })
  }
})