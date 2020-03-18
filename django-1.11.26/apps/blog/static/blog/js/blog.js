/**
 * Created by Weic on 2017/6/8.
 */
// Pjax用其他脚本封装函数
function config() {

// 文章页标签云随机色
var tag_cloud = $('.blog-post-page-tags>a');
tag_cloud.each(function () {
    var Cnum = 9;
    var Crand = parseInt(Math.random() * Cnum);
    $(this).addClass("tag-could" + Crand);
})


// 限制博客盒子的最低高度为浏览器可视区高度
$('.blog-main').css('min-height',$(window).height());


// 给文章页input添加class
$('.blog-post-page-content input').addClass('form-control');


// 返回顶部
function backTop() {
    var DomscrollTop = $(document).scrollTop();
    if (DomscrollTop > 450) {
        $(".retop").css("display", "block");
    } else {
        $(".retop").css("display", "none");
    }
    setTimeout(backTop)
}
backTop();
$(".retop").click(function() {
    $('html,body').animate({
            scrollTop: 0
        },
        400)
});


// 博客侧栏网站标题
function blogTitle() {
    var DomscrollTop = $(document).scrollTop();
    if (DomscrollTop > 10){
        $('.blog-sidebar-title').addClass('blog-sidebar-title-shadow');
    }else{
        $('.blog-sidebar-title').removeClass('blog-sidebar-title-shadow');
    }
    setTimeout(blogTitle);
}
blogTitle();


// 移动端导航
$(".blog-header-navbar-btn").click(function () {
    $(".blog-header-navbar").slideToggle("slow");
}) 

// 标签提示
$('.tag-could,.blog-post-page-readmore>a,.blog-post-page-tags>a,.blog-sidebar-icon>ul>li>a,.btn').tooltip();

// 图像查看器插件
$(".blog-post-page-content img:not('.no-lightbox')").each(function(){
    var imgSrc = $(this).attr('src');
    $(this).wrap("<a class='img-a img-group' data-fancybox='group' href='javascript:;'></a>");
    $(this).parent().attr('href',imgSrc);
})

//给文章页a标签添加target='_blank'属性 ，开启之后在文章详情页点击标签会打开新页面，取消后为当前为页面内跳转
//$(".blog-post-page-content a:not('.img-a')").attr('target','_blank');

// 链接页面类名
$('.links-block>a').addClass('links-block-btn btn btn-outline-info btn-block').wrap('<div class="col-md-3 links-block-div"></div>');
$('.links-block').addClass('row');

}
// 表格滚动条,父元素宽度不足时显示横向滚动条，避免表格撑破布局
$("table").wrap("<section class='table-area'></section >");


// 鼠标点击自动显示爱心效果，多种颜色love.js
!function(e, t, a) {
    function n() {
        c(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),
        o(),
        r()
    }
    function r() {
        for (var e = 0; e < d.length; e++) d[e].alpha <= 0 ? (t.body.removeChild(d[e].el), d.splice(e, 1)) : (d[e].y--, d[e].scale += .004, d[e].alpha -= .013, d[e].el.style.cssText = "left:" + d[e].x + "px;top:" + d[e].y + "px;opacity:" + d[e].alpha + ";transform:scale(" + d[e].scale + "," + d[e].scale + ") rotate(45deg);background:" + d[e].color + ";z-index:99999");
        requestAnimationFrame(r)
    }
    function o() {
        var t = "function" == typeof e.onclick && e.onclick;
        e.onclick = function(e) {
            t && t(),
            i(e)
        }
    }
    function i(e) {
        var a = t.createElement("div");
        a.className = "heart",
        d.push({
            el: a,
            x: e.clientX - 5,
            y: e.clientY - 5,
            scale: 1,
            alpha: 1,
            color: s()
        }),
        t.body.appendChild(a)
    }
    function c(e) {
        var a = t.createElement("style");
        a.type = "text/css";
        try {
            a.appendChild(t.createTextNode(e))
        } catch(t) {
            a.styleSheet.cssText = e
        }
        t.getElementsByTagName("head")[0].appendChild(a)
    }
    function s() {
        return "rgb(" + ~~ (255 * Math.random()) + "," + ~~ (255 * Math.random()) + "," + ~~ (255 * Math.random()) + ")"
    }
    var d = [];
    e.requestAnimationFrame = function() {
        return e.requestAnimationFrame || e.webkitRequestAnimationFrame || e.mozRequestAnimationFrame || e.oRequestAnimationFrame || e.msRequestAnimationFrame ||
        function(e) {
            setTimeout(e, 1e3 / 60)
        }
    } (),
    n()
} (window, document);




