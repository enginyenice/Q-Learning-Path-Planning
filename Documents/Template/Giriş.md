#  [<< Ödev Belgesi](../Project%20Requirements/Yazlab2-Proje3.pdf)
# Giriş

Pekiştirmeli öğrenmede ajan (agent) adı verilen öğrenen makinemiz karşılaştığı durumlara bir tepki verir ve bunun karşılığında da sayısal bir 
ödül sinyali alır. Ajan/öğrenen makine aldığı bu ödül puanını maksimuma  çıkartmak için çalışır. Bu şekilde çalışan deneme yanılma yöntemi (brute force), pekiştirmeli öğrenmenin en ayırt edici özelliğidir.

>  Pekiştirmeli öğrenme bir problem hakkında çalışma ve çözüm yöntemidir.

Pekiştirmeli Öğrenme (Reinforcement learning) algoritması Markov karar süreci 
denilen bir model kullanmaktadır.
Markov karar süreçlerinin en önemli 3 özelliği;
1. Algılama (sensation)
2. Eylem (action)
3. Hedef (goal)


Pekiştirmeli öğrenme (Reinforcement learning)  sürecindeki en önemli zorluklar, keşif (exploration) ve sömürü (exploitation) kavramlarının uygulamaya geçirilmesidir. Ajanın (Agent) daha fazla ödül elde etmesi için geçmişte
denediği ve pozitif ödül aldığı eylemleri seçmelidir. Ajan ödül elde etmek için daha önce deneyimlediği eylemleri seçmelidir. Ajan (Agent) ödül elde etmek için daha önce deneyimlediği eylemlerden yararlanır, ancak karşılaştığı bir durumda daha fazla ödül alabileceği eylemler varsa bunları da keşfetmelidir. Böylece 
Ajan(Agent), çeşitli eylemler denemeli ve en iyi sonuç/ödül alabildiklerini aşamalı olarak desteklemelidir.

Tüm pekiştirmeli öğrenme ajanları açık hedeflere sahip olup çevrenin  özelliklerini algılayabilir ve çevrelerini etkileyebilecek eylemleri seçebilirler. 
##  Pekiştirmeli Öğrenme Ögeleri

Bir Pekiştirmeli Öğrenme sisteminde ajan ve çevre (environment) dışında biri 
opsiyonel olmak üzere dört unsur bulunur:

1. Politika (policy)
2. Ödül (reward signal)
3. Değer/Durum Değeri (value function)
4. Çevre modeli (model)

### Politika
Ajanın içinde bulunduğu durumda alabileceği aksiyonu belirler. 
Bir nevi etki-tepki eşleşmesi olarak düşünülebilir. İçinde bulunulan durum bir 
etki olarak kabul edilirse ajan buna karşılık bir tepki (action) verir. 
Bu politika basit bir aksiyon olarak tanımlanabileceği gibi bütün durumları 
karşılayan bir arama tablosu şeklinde de tanımlanabilir. Politika dinamik olarak 
da nitelenebilir. Bunun temel nedeni, ajanın içinde bulunduğu durumu 
değerlendirerek alabileceği aksiyonları aramasından (farkına varmasından) 
kaynaklanmaktadır.

### Ödül
Ajanının gerçekleştirmiş olduğu bir aksiyona karşılık çevreden aldığı 
puandır. Bir pekiştirmeli öğrenme ajanının amacı, uzun vadede aldığı ödülleri 
maksimum seviyeye ulaştırmaktır. Ödül alınan aksiyonun ne kadar iyi veya kötü 
olduğunu belirleyen değerdir (basit bir şekilde mutluluk veya acı ile 
eşleştirilebilir). Ajan, izlemiş olduğu politikayı bu ödülleri esas alarak zaman 
içerisinde değiştirir. Örneğin alınan bir aksiyonun sonrasında düşük bir puan 
elde ediliyorsa, gelecekte ajan aynı duruma geldiğinde farklı bir aksiyon almayı 
tercih edebilir.

### Durum değeri
Ajanın içinde bulunduğu durumdan ve o durumu takip eden diğer 
durumlardan bekleyebileceği ödüllerin toplamıdır. Ödüller anlık olarak neyin iyi 
neyin kötü olduğunu ifade ederken, durum değeri uzun vadede neyin iyi neyin kötü 
olduğunu ifade eder. Örneğin; bir durum, düşük bir ödüle fakat yüksek bir değere 
sahip olabilir. Bunun nedeni düşük ödül veren durumu takip eden yüksek ödüllü 
diğer durumlardır. Tam tersi de mümkündür. Yüksek ödül veren bir durumdan sonra 
sürekli olarak düşük ödüller veren durumlar da olabilir. Buradaki durum 
“ileri görüşlülük” gibi düşünülebilir.

### Çevre modeli (model)
Son unsurumuz olan model ise, isteğe bağlı olarak sisteme dahil edilen bir 
unsurdur. Çevrenin bir simülasyonu olup ajanın bir aksiyonu gerçekleştirmeden 
önce bu aksiyon sonucunda alabileceği ödülü ve doğuracağı durumu tahmin etmesini 
sağlamaktadır. Bu sayede bir planlama yapılarak ajanın davranışında değişiklik 
meydana gelebilecektir.

## Kapsam ve Sınırlamalar
Pekiştirmeli Öğrenme, yoğun bir şekilde durum(state) kavramına dayanmaktadır. 
Politika ve değer fonksiyonunda girdi olarak kullanılırken; modelde ise hem 
girdi hem de çıktı olarak kullanılmaktadır.


# [>> Yöntem](Yontem.md)
