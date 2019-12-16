/**
 * Created by nextgo on 2017/10/18 0018.
 */
//url解析
function url_parse(url) {
    var url_dict = {
        host:null,
        path:null,
        querys:{},
    };
    var path = null,
        querys = null;

    if(url.split("//").length === 2){
        //说明开头是有主机名的
        url = url.split("//")[1];

        var parts = url.split("/");
        url_dict.host = parts.splice(0, 1)[0];
        url = "/" + parts.join("/");
    }




    if(url.split("?").length === 2){
        path = url.split("?")[0];
        querys = url.split("?")[1];
    }else{
        path = url.split("?")[0];
    }

    url_dict.path = path;

    if(typeof querys === "string"){
        $.each(querys.split("&"),function(i,query){
            url_dict.querys[query.split("=")[0]] = decodeURI(query.split("=")[1]);
        });
    }

    return url_dict;
}
//url反解析
function url_unparse(url_dict) {
    //如果有host，必须在前面加//
    var url = "";
    var query_list = []

    if(url_dict.host){
        url += "//" + url_dict.host;
    }

    url += url_dict['path']+"?";
    $.each(url_dict.querys,function (k,v) {
        query_list.push(k+"="+encodeURI(v));
    });
    url += query_list.join("&");
    return url
}

//添加参数
function add_query(url,dict){
    var url_dict = url_parse(url);

    $.each(dict,function (k,v) {
        url_dict["querys"][k] = v;
    });

    url = url_unparse(url_dict);
    return url;
}