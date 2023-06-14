let post_data = data[0].fields;
$(document).ready(function () {
    $("#like").click(function (e) {
        console.log('edit-like');
        make_req('POST', '/post/updatePost/', {
            'post_id': data[0].pk,
            'update_type': 'like'
        }, function (data) {
            if (!data.is_like) {
                $('#like').html(`<img src="/static/images/liked.svg" width="32px" height="32px" alt="">`);
            }
            else {
                $('#like').html(`<img src="/static/images/like.svg" width="32px" height="32px" alt="">`);
            }
            $('#likes-count').text(data.likes_count + ' likes');
        });
    });
    $("#comment").click(function (e) {
        e.preventDefault();
        make_req('POST', '/post/updatePost/', {
            'post_id': data[0].pk,
            'update_type': 'comment',
            'comment': $('#comment-input').val()
        }, function (data) {
            $('#comment-section').empty();
            $('#comment-input').val('');
            data.map((element, index) => {
                $('#comment-section').append
                    (`
                    <div class="card mb-4">
                        <div class="card-body">
                            <p>${element.comment}</p>
                            <div class="d-flex justify-content-between">
                                <div class="d-flex flex-row align-items-center">
                                    <img class="rounded-circle" width="32px" height="32px" src=${element.user_pic}
                                    alt="avatar" style="object-fit: cover;"/>
                                    <a href="/${element.user_name}/" class="small mb-0 ms-2 ">${element.user_name}</a>
                                </div>
                                <div class="d-flex flex-row align-items-center">
                                    <p class="small text-muted mb-0">${element.time_ago}</p>
                                    <a id="like-${index}" type="submit" class="btn-sm"><img src="/static/images/like.svg" width="20px"
                                        height="20px" alt=""></a>
                                    <a type="button" class="btn-sm"><img
                                        src="/static/images/comment.svg" width="20px" height="20px" alt=""></a>
                                </div>
                            </div>
                        </div>
                    </div>
                `)
            });
        });
    });
    $("#caption-edit").click(function (e) {
        console.log('edit-caption');
        make_req('POST', '/post/updatePost/', {
            'post_id': data[0].pk,
            'update_type': 'caption',
            'caption': $('#caption-input').val()
        }, function (data) {
            
        });
    });
});