// var opened = false;
// var select = $("select");
//
//
// select.on("click", function () {
//     if (!opened) {
//         $("#CheckForm").submit()
//         opened = true;
//     }
// });
//
// select.on("change", function () {
//     $("#CheckForm").submit()
//     setTimeout(function () {
//         opened = false;
//     }, 0);
// });
//

function ScanningLabel(){
    $("#scanning_span").text('Scanning Network...')
}
function ConfiguringSNMP(){
    $("#configure_span").text('Configuring SNMPv3...')
}

