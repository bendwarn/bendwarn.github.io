---
layout: post
comments: true
title: Red Black Tree In Functional Programming
---
本文介紹 FP 如何實作紅黑樹的新增和刪除，如果不清楚紅黑樹是什麼，或忘記如何 imperatively 操作紅黑樹，可以先到[紅黑樹介紹](http://alrightchiu.github.io/SecondRound/red-black-tree-introjian-jie.html)獲得來龍去脈。

好的，知道那些奇怪的操作之後，可以忘掉了，因為 FP 用不到。

##### 新增
到底要怎麼講解新增，我想了很久，但我看不出來有什麼文字比這張圖更能解釋程式在幹嘛的。（參考資料 2 有 haskell 程式。）
![insertion balance](https://i.imgur.com/WiPyDZO.png){:height="75%" width="75%"}

非常精妙的將全部 case 整理成四種情況，並且歸一到相同解！

##### 刪除
真正的困難藏在這裡，往下讀之前可以試試看：你現在知道多一個紅的要怎麼平衡，思考一下少一個黑的如何平衡？

解法的核心在於引入兩個新顏色，深黑與負黑，分別代表 +2, -1。（你可能記得紅黑樹每條路徑的黑點數量要相同，換句話說這些顏色其實是計數器，黑跟紅代表 1 跟 0）接著運用 divide and conquer 分成三個步驟：

1. remove：當你移除末端的黑點時就會用到深黑。
2. bubble：將深黑狀態往上傳，因為在底部沒有子節點來平衡這個顏色。這個步驟很簡單，把子節點 -1、父節點 +1 即可。
3. balance：在這個過程尋找消除的機會。

即使多兩個顏色，也只多出六種情況，最美妙的是，其中四種可以照抄新增的！
剩下的則負責將左圖變成右圖

![BB NB](http://matt.might.net/articles/red-black-delete/images/red-black-slides.018.png) | ![eliminate](http://matt.might.net/articles/red-black-delete/images/red-black-slides.019.png)

其餘的就是一些有關刪除的 helper function，你的作業就寫完啦！（誰會把這個當作業啊，還有人性嗎？）

## 後記
會想做這個的初衷是為了製作測試腦袋是否清醒的石蕊試紙，突發奇想覺得如果能正確心算操作紅黑樹的話，那腦袋大概就是清醒的（想到這種點子的時候大概是不清醒的）。同時想順便練習 elm，於是 project 就這麼開始了。樹的呈現花了一點心思，因為我也沒用過 svg，要查一下；拉線方式也從一開始的固定角度變成直接算座標。重頭戲果然還是在演算法。我過於拘泥原本作法，想了很久還是想不出來，問神之後就找到那兩篇論文。

寫完之後才發現，根本沒用嘛，操作麻煩只存在於 imperative 啊，變成這樣就算喝醉也能心算新增和刪除了吧。

###### 參考資料：
1. <https://wiki.rice.edu/confluence/download/attachments/2761212/Okasaki-Red-Black.pdf>
2. <http://matt.might.net/articles/red-black-delete>
