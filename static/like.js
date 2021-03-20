$(document).on("click",".like-btn", function(e) {
  e.preventDefault()
  const this_ = $(this);
  console.log(this_)
  const data_id = this_.attr("data-id")
  const like_cnt = $("#like"+data_id);
  const likeUrl = this_.attr("data-href");
  if (likeUrl){
    $.ajax({
      url: likeUrl,
      method: "GET",
      data: {"status":1}, //　いいねが押されましたと伝える
    })
    .then(
      function(data){
        let change_like = Number(like_cnt.text());
        if (data.liked){　//　もしいいねされていなかったら
          like_cnt.text(++change_like);　//　いいねの数を１追加
          this_.addClass("on");　//　ボタンをピンクに
        } else {　　//　もしいいねされていたら
          like_cnt.text(--change_like);　//　いいねの数を１減らす
          this_.removeClass("on");　//　ボタンのデザインを初期状態に
        }
      },
      function(error){
        console.log("エラーが発生しました")
      }
    )
  } else {
    window.alert("エラーが発生しました。URLが不明です。")
  }
})