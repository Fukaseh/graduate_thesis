import yaml
import os

def makeplt(plot_name, str_ask, str_bid):
    gnuplot_code = f"""set terminal pdfcairo enhanced font "Helvetica,18"
set output "output_pdf_gnu/{plot_name}_a{str_ask}_b{str_bid}.pdf"
set log y
set log x
set format xy "10^{"{%T}"}"
set yrange [1e-3:1]
set key left bottom
set style data lines
p 'output_dat/{plot_name}_a{str_ask}_b{str_bid}.dat' using 1:2 with line lw 8 lc rgb 'blue' title "{plot_name}", \\
  'output_dat/{plot_name}_a{str_ask}_b{str_bid}.dat' using 3:4 with line lw 8 lc rgb 'red' title 'N(0, 1)'
"""

    # a.pltファイルを作成して書き込む
    with open(f'plt/{plot_name}_a{str_ask}_b{str_bid}.plt', 'w') as f:
        f.write(gnuplot_code)


# task.shの既存の内容を消去
with open('task.sh', 'w') as task_file:
    pass 
with open('task2.sh', 'w') as task2_file:
    pass


# askを何種類か、bidを何種類か
asks = [0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.5]
bids = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

for a in range(len(asks)):
    for b in range(len(bids)):
        # yamlファイルに書き込む内容を保存
        bid_ask_info = {
            "maxAsk": asks[a],
            "maxBid": bids[b]
        }

        # 保存先をyamlフォルダにする
        folder = "./yaml"
        # ファイルの名前をつける
        str_ask = str(asks[a]).replace(".","")
        str_bid = str(bids[b]).replace(".","")
        file_name = os.path.join(folder, f"a{str_ask}_b{str_bid}.yaml")
        
        # yamlファイルの作成
        with open(file_name,'w') as file:
            yaml.dump(bid_ask_info, file, default_flow_style=False, allow_unicode=True)
        
        # task.shに実行するためのコマンドを書いていく
        with open('task.sh', 'a') as task_file:
            task_file.write(f"python3 script.py {file_name}\n")
        
        plot_name1 = "asset"
        plot_name2 = "asset_growth"
        plot_name3 = "price"

        # 生存関数を描画するためのpltファイルの作成
        makeplt(plot_name1,str_ask, str_bid)
        makeplt(plot_name2, str_ask, str_bid)
        makeplt(plot_name3, str_ask, str_bid)

        # task2.shに実行するためのコマンドを書いていく
        with open('task2.sh', 'a') as task2_file:
            task2_file.write(f"gnuplot ./plt/{plot_name1}_a{str_ask}_b{str_bid}.plt\n")
            task2_file.write(f"gnuplot ./plt/{plot_name2}_a{str_ask}_b{str_bid}.plt\n")
            task2_file.write(f"gnuplot ./plt/{plot_name3}_a{str_ask}_b{str_bid}.plt\n")

