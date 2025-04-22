import re
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
from time import sleep

#今の日時を定義
now = datetime.now()
formatter_date_time = now.strftime("%Y-%m-%d %H:%M")


def test_state_transition_diagram():
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

        #状態遷移図生成
        page.get_by_test_id("create").click()
        page.get_by_text("状態遷移テスト").click()
        expect(page.get_by_role("textbox", name="名前 名前")).to_have_value("無題の状態遷移テスト");

        #状態遷移図名前変更
        page.get_by_role("textbox", name="名前 名前").click()
        page.get_by_role("textbox", name="名前 名前").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="名前 名前").fill("変更した名前")
            #１秒待機
        sleep(1)
        page.get_by_test_id("back").click()
        page.get_by_role("button", name="state_transition 変更した名前").click()

        #ノード,遷移追加

        #状態遷移表とテストケースの出力
        page.locator("#select-box-with-chips i").click()
        page.get_by_role("option", name="1スイッチ").click()
        page.get_by_test_id("state-gen").click()
        expect(page.get_by_text("状態遷移表 (状態×イベント)save_alt CSVダウンロード Start buttonStop buttonReset")).to_be_visible()
        expect(page.get_by_text("状態遷移表 (前状態×後状態)save_alt CSV")).to_be_visible()
        expect(page.get_by_text("無効遷移を含めた全遷移テストケースsave_alt CSV")).to_be_visible()
        expect(page.get_by_text("1スイッチ テストケースsave_alt CSV")).to_be_visible()


        #CSVダウンロード
        with page.expect_download() as download_info:
            page.get_by_role("button", name="CSVダウンロード").first.click()
        download = download_info.value
            #ダウンロードされたファイル名を取得
        downloaded_file_name = download.suggested_filename
            #ファイル名確認
        date_format_regex = r'\d{4}-\d{2}-\d{2}'
        expected_file_name_pattern = rf"State-transition-table_state_event_{date_format_regex}\.csv"

        #PNGダウンロード
        page.get_by_test_id("downloadDiagramBtn").click()
        with page.expect_download() as download1_info:
            page.get_by_text("PNG形式").click()
        download1 = download1_info.value
            #ダウンロードされたファイル名を取得
        downloaded_file_name = download.suggested_filename
            #ファイル名確認
        date_format_regex = r'\d{4}-\d{2}-\d{2}'
        expected_file_name_pattern = rf"state-transition-diagram\.png"

        #自動保存OFF時保存確認
        page.get_by_role("textbox", name="名前 名前").click()
        page.get_by_role("textbox", name="名前 名前").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="名前 名前").fill("変更後の名前自動保存OFF")
        page.get_by_role("checkbox", name="自動保存ON").uncheck()
        expect(page.get_by_role("checkbox", name="自動保存OFF")).not_to_be_checked()
        page.get_by_test_id("save").click()
        page.get_by_test_id("back").click()
        page.get_by_role("button", name="state_transition 変更後の名前自動保存OFF").click()

        #状態遷移テスト削除
        page.get_by_role("checkbox", name="自動保存OFF").check()
        page.locator("div").filter(has_text=re.compile(r"^保存$")).get_by_role("button").nth(1).click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_text("削除").click()

        page.goto("https://gihoz.com/users/dl_auto_test_support/repositories/test_PoC/folders/626577c0-3a90-4777-9b2a-ac74619ab3e9")
        expect(page.locator("#test-model-case-table")).to_match_aria_snapshot("- textbox\n- table:\n  - rowgroup:\n    - row \"名前 種類 更新日時 更新者\":\n      - cell \"名前\"\n      - cell \"種類\"\n      - cell \"更新日時\"\n      - cell \"更新者\"\n  - rowgroup:\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n- separator\n- text: \"1ページあたりの表示件数:\"\n- combobox:\n  - text: /\\d+/\n  - textbox: /\\d+/\n- text: 1-4件/全4件中\n- navigation \"ページネーション\":\n  - list:\n    - listitem:\n      - button \"最初のページ\" [disabled]\n    - listitem:\n      - button \"前のページ\" [disabled]\n    - listitem:\n      - button \"次のページ\" [disabled]\n    - listitem:\n      - button \"最後のページ\" [disabled]")

        # ---------------------
        context.close()
        browser.close()