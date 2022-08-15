clear;
close all;

%x軸數值
x = 5:5:20;

%{
y軸數值
Mi_mean = [4.996754966887418, 9.944999999999999, 14.945789473684211, 19.134802631578946, 18.597631578947368, 17.81809210526316, 15.610272108843537, 15.086730769230769];
Mi_std = [0.06263704621467145, 0.6105886856520989, 1.0429546200535822, 2.2966286752642473, 3.0706922093925306, 2.19574565577116, 4.178046824524037, 4.391261499601113];

Mo_mean = [4.9959602649006625, 7.9440624999999985, 7.100158730158731, 7.705662650602411, 7.622702702702702, 7.660923076923076, 7.31857142857143, 7.441363636363636];
Mo_std = [0.18747152248789514, 2.1725510487007034, 2.1342064265605973, 1.7725069697968057, 1.7179761087988255, 1.6372659404065621, 1.6210284801117263, 1.4433352700958804];

No_mean = [4.989230769230769, 3.3380199999999998, 2.6008562500000005, 4.091428282828283, 4.014650561797752, 3.5482800000000005, 3.6861639344262294, 3.3478474576271187];
No_std = [0.1779363367903594, 1.841302845102497, 1.7108990810309184, 1.5934805506545626, 1.582614515397313, 1.740273248166998, 1.5961272319829634, 1.6532658256078285];

Ma_mean = [3.589870129870129, 2.188983660130719, 1.7372178294573641, 2.6636082474226805, 2.5634626373626372, 2.3754166666666667, 2.486963492063492, 2.1554841269841267];
Ma_std = [0.1349073127132567, 1.2031226290725794, 1.1651736478317307, 1.0124491916953684, 1.0880479387568212, 1.1373080583016686, 1.1237311273382522, 1.176228715717937];
%}

NSDAR_Mi_mean = [4.996754966887418, 9.944999999999999, 14.945789473684211, 19.134802631578946];
NSDAR_Mi_std = [0.06263704621467145, 0.6105886856520989, 1.0429546200535822, 2.2966286752642473];

NSDAR_Mo_mean = [4.9959602649006625, 7.9440624999999985, 7.100158730158731, 7.705662650602411];
NSDAR_Mo_std = [0.18747152248789514, 2.1725510487007034, 2.1342064265605973, 1.7725069697968057];

NSDAR_No_mean = [4.989230769230769, 3.3380199999999998, 2.6008562500000005, 4.091428282828283];
NSDAR_No_std = [0.1779363367903594, 1.841302845102497, 1.7108990810309184, 1.5934805506545626];

NSDAR_Ma_mean = [3.589870129870129, 2.188983660130719, 1.7372178294573641, 2.6636082474226805];
NSDAR_Ma_std = [0.1349073127132567, 1.2031226290725794, 1.1651736478317307, 1.0124491916953684];

NSR_Mi_mean = [4.997947019867552, 9.87461842105263, 13.467071895424839, 13.484522875816994];
NSR_Mi_std = [0.08027716886549748, 2.087574849938441, 3.738544812780163, 4.921604021643232];

NSR_Mo_mean = [4.970657894736842, 6.4513449275362325, 5.470627906976745, 4.719287786259542];
NSR_Mo_std = [0.3599184437652868, 3.349306010741213, 2.7311830542990188, 2.827540725436775];

NSR_No_mean = [4.979933774834437, 3.7673776119402986, 3.2265703125, 2.891952845528455];
NSR_No_std = [0.2947665668258907, 1.9173040456340722, 1.6305904233974553, 1.631333430820422];

NSR_Ma_mean = [3.580909090909091, 2.458845925925926, 2.049174418604651, 1.8848390243902438];
NSR_Ma_std = [0.10991597287603747, 1.1602597155708552, 1.0952059250061628, 1.0476833695782537];

%將曲線圖上加上標準差並且重疊所有線
figure;errorbar(x, NSDAR_Mi_mean, NSDAR_Mi_std, 'r--O');hold on
errorbar(x, NSDAR_Mo_mean, NSDAR_Mo_std, 'g--*');hold on
errorbar(x, NSDAR_Ma_mean, NSDAR_Ma_std, 'b--square' );hold on
errorbar(x, NSDAR_No_mean, NSDAR_No_mean, 'm--diamond');hold on
errorbar(x, NSR_Mi_mean, NSDAR_Mi_std, 'r-O');hold on
errorbar(x, NSR_Mo_mean, NSDAR_Mo_std, 'g-*');hold on
errorbar(x, NSR_Ma_mean, NSDAR_Ma_std, 'b-square' );hold on
errorbar(x, NSR_No_mean, NSDAR_No_mean, 'm-diamond');
%限制軸的刻度
xlim([0 25]);ylim([0 30]);

%標示軸的單位(名稱)
xlabel('Sent Bandwidth(Mbits/sec)');ylabel('Received Bandwidth(Mbits/sec)');

%標示曲線名稱
legend('Mission-critical IoT','Mobile Broadband','Massive IoT','Default Path')