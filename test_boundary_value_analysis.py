import re
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
from time import sleep

#今の日時を定義
now = datetime.now()
formatter_date_time = now.strftime("%Y-%m-%d %H:%M")


def test_boundary_value_analysis():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        #ログイン
        page.goto("https://gihoz.com/login?fullPath=%2Frepositories")
        page.get_by_role("button", name="ベリサーブIDでログイン").click()
        page.get_by_role("textbox", name="メールアドレス").click()
        page.get_by_role("textbox", name="メールアドレス").fill("dl_auto_test_support@veriserve.co.jp")
        page.get_by_role("textbox", name="パスワード").click()
        page.get_by_role("textbox", name="パスワード").fill("G1hoz@utosup1234")
        page.get_by_role("button", name="続ける").click()
        page.get_by_test_id("test_PoC").get_by_text("dl_auto_test_support/test_PoC").click()
            #ダイヤログに対する準備
        page.on('dialog', lambda dialog: dialog.accept())

        #境界値分析を生成
        page.get_by_test_id("create").click()
        page.get_by_text("境界値分析").click()

        #名前変更確認
        expect(page.get_by_role("textbox", name="名前 名前")).to_have_value("無題の境界値分析");
        page.get_by_role("textbox", name="名前 名前").click()
        page.get_by_role("textbox", name="名前 名前").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="名前 名前").fill("変更した名前")
            #１秒待機
        sleep(1)
        page.get_by_test_id("back").click()
        page.get_by_role("button", name="boundary_value 変更した名前").click()

        #変数を追加
        page.get_by_test_id("add-number-line").click()
        page.get_by_test_id("text-field-of-variable-name").get_by_role("textbox", name="名前 名前").click()
        page.get_by_test_id("text-field-of-variable-name").get_by_role("textbox", name="名前 名前").fill("変数1")
        page.get_by_role("textbox", name="値の増減幅 値の増減幅").dblclick()
        page.get_by_role("textbox", name="値の増減幅 値の増減幅").fill("1")
        page.get_by_role("textbox", name="最小値 最小値").click()
        page.get_by_role("textbox", name="最小値 最小値").fill("0")
        page.get_by_role("textbox", name="最大値 最大値").click()
        page.get_by_role("textbox", name="最大値 最大値").fill("10")
            #１秒待機
        sleep(1)
        page.get_by_test_id("dialog-confirm").click()
        expect(page.get_by_text("名前名前3 / 100削除010変数を追加同値パーティション一覧を表示")).to_be_visible()

        #変数名の変更
        page.get_by_test_id("boundary1").get_by_role("textbox", name="名前 名前").click()
        page.get_by_test_id("boundary1").get_by_role("textbox", name="名前 名前").press("ControlOrMeta+a")
        page.get_by_test_id("boundary1").get_by_role("textbox", name="名前 名前").fill("変数10")
        page.get_by_text("数直線").click()
        expect(page.get_by_test_id("boundary1").get_by_role("textbox", name="名前 名前")).to_have_value("変数10");

        #境界の追加
        page.locator("div:nth-child(17) > div > .valid-circle-default > div > .v-card").click()
        page.get_by_role("textbox", name="数値 数値").click()
        page.get_by_role("textbox", name="数値 数値").fill("5")
        page.get_by_test_id("boundary-confirm").click()
        expect(page.locator("#base-doc")).to_match_aria_snapshot("- textbox \"名前 名前\"\n- alert\n- button \"削除\"\n- textbox: 新しい同値パーティション\n- textbox: 新しい同値パーティション\n- text: /0 4 5 \\d+/\n- button \"変数を追加\"\n- button \"同値パーティション一覧を表示\"")

        #同値パーティション一覧を表示
        page.get_by_test_id("partition-list-btn").click()
        expect(page.get_by_text("変数10save_alt CSV")).to_be_visible()

        #同値パーティション一覧を更新
        page.get_by_role("textbox").nth(2).click()
        page.get_by_role("textbox").nth(2).press("ControlOrMeta+a")
        page.get_by_role("textbox").nth(2).fill("変更した同値パーティション1")
        page.get_by_role("textbox").nth(2).click()
        page.get_by_role("textbox").nth(3).click()
        page.get_by_role("textbox").nth(3).press("ControlOrMeta+a")
        page.get_by_role("textbox").nth(3).fill("変更した同値パーティション2")
        page.get_by_role("textbox").nth(3).click()
        page.get_by_test_id("partition-list-btn").click()
        expect(page.get_by_text("変数10save_alt CSV")).to_be_visible()

        #CSVダウンロード
        with page.expect_download() as download_info:
            page.get_by_role("button", name="CSVダウンロード").click()
        download = download_info.value
            #ダウンロードされたファイル名を取得
        downloaded_file_name = download.suggested_filename
            #ファイル名確認
        date_format_regex = r'\d{4}-\d{2}-\d{2}'
        expected_file_name_pattern = rf"Equivalence-partition-lists_変数10_{date_format_regex}\.csv"

        #テストケース生成
        page.get_by_test_id("testcase-gen").click()
        expect(page.get_by_test_id("testcase-list")).to_be_visible()

        #変数削除
        page.get_by_role("button", name="削除").click()
        page.get_by_test_id("msg-dlg-delete-btn").click()
        expect(page.get_by_text("変数を追加同値パーティション一覧を更新")).to_be_visible()

        #テストケース削除
        page.locator("div").filter(has_text=re.compile(r"^保存$")).get_by_role("button").nth(1).click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_text("削除").click()

        page.goto("https://gihoz.com/users/dl_auto_test_support/repositories/test_PoC/folders/626577c0-3a90-4777-9b2a-ac74619ab3e9")
        expect(page.locator("#test-model-case-table")).to_match_aria_snapshot("- textbox\n- table:\n  - rowgroup:\n    - row \"名前 種類 更新日時 更新者\":\n      - cell \"名前\"\n      - cell \"種類\"\n      - cell \"更新日時\"\n      - cell \"更新者\"\n  - rowgroup:\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n- separator\n- text: \"1ページあたりの表示件数:\"\n- combobox:\n  - text: /\\d+/\n  - textbox: /\\d+/\n- text: 1-4件/全4件中\n- navigation \"ページネーション\":\n  - list:\n    - listitem:\n      - button \"最初のページ\" [disabled]\n    - listitem:\n      - button \"前のページ\" [disabled]\n    - listitem:\n      - button \"次のページ\" [disabled]\n    - listitem:\n      - button \"最後のページ\" [disabled]")




        # ---------------------
        context.close()
        browser.close()

