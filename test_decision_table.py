import re
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
from time import sleep

#今の日時を定義
now = datetime.now()
formatter_date_time = now.strftime("%Y-%m-%d %H:%M")


def test_decision_table_creation():
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

        #デシジョンテーブル生成
        page.get_by_test_id("create").click()
        page.get_by_test_id("create-decisiontable").get_by_text("デシジョンテーブルテスト").click()
        expect(page.get_by_role("textbox", name="名前 名前")).to_have_value("無題のデシジョンテーブルテスト");

        #デシジョンテーブル名前変更
        page.get_by_role("textbox", name="名前 名前").click()
        page.get_by_role("textbox", name="名前 名前").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="名前 名前").fill("変更した名前")

        #デシジョンテーブル名前変更確認
        page.get_by_test_id("back").click()
        expect(page.get_by_test_id("変更した名前").get_by_role("button")).to_match_aria_snapshot("- text: 変更した名前")
        page.get_by_role("button", name="decision_table 変更した名前").click()

        #条件部入力
        page.get_by_role("row", name="条件 ", exact=True).get_by_role("gridcell").nth(1).click()
        page.get_by_role("row", name="条件 ", exact=True).get_by_role("gridcell").nth(1).dblclick()
        page.get_by_role("textbox").nth(2).fill("条件①")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()

        expect(page.get_by_title("サブ条件を追加").nth(1)).to_be_visible()
        page.get_by_title("条件を追加").nth(2).click()
        expect(page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(4) > td:nth-child(2)")).to_be_visible()

        page.get_by_title("サブ条件を追加").nth(1).click()
        expect(page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(4) > td:nth-child(3)")).to_be_visible()
        page.get_by_role("row", name="条件  条件① ", exact=True).get_by_role("gridcell").nth(2).dblclick()
        page.get_by_role("textbox").nth(1).fill("条件①ーC")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()
        expect(page.get_by_role("gridcell", name="条件①ーC").nth(1)).to_be_visible()


        #動作部入力
        page.get_by_role("row", name="動作 ", exact=True).get_by_role("gridcell").nth(1).click()
        page.get_by_role("row", name="動作 ", exact=True).get_by_role("gridcell").nth(1).dblclick()
        page.get_by_role("textbox").nth(2).click()
        page.get_by_role("textbox").nth(2).fill("動作①")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()

        expect(page.get_by_title("サブ動作を追加").nth(1)).to_be_visible()
        page.get_by_title("動作を追加").nth(2).click()
        expect(page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(7) > td:nth-child(2)")).to_be_visible()

        page.get_by_title("サブ動作を追加").nth(1).click()
        expect(page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(7) > td:nth-child(3)")).to_be_visible()
        page.get_by_role("row", name="動作  動作① ", exact=True).get_by_role("gridcell").nth(2).dblclick()
        page.get_by_role("textbox").nth(1).fill("動作①ーC")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()
        expect(page.get_by_role("gridcell", name="動作①ーC").nth(1)).to_be_visible()

        #条件部Y記入
        page.get_by_role("row", name="条件  条件①  条件①ーC -").get_by_role("gridcell").nth(3).dblclick()
        page.get_by_role("option", name="Y").click()

        #条件部N記入
        page.get_by_role("gridcell", name="-").first.click()
        page.get_by_role("gridcell", name="-").first.dblclick()
        page.get_by_role("option", name="N").click()

        #動作部X記入
        page.get_by_role("gridcell", name="-").nth(1).click()
        page.get_by_role("gridcell", name="-").nth(1).dblclick()
        page.get_by_role("option", name="X").click()

        #動作部-記入
        page.get_by_role("gridcell", name="-").nth(1).click()
        page.get_by_role("gridcell", name="-").nth(1).dblclick()
        page.get_by_role("option", name="-").click()

        #YNX-入力確認
        expect(page.get_by_role("gridcell", name="Y")).to_be_visible()
        expect(page.get_by_role("gridcell", name="N")).to_be_visible()
        expect(page.get_by_role("gridcell", name="X")).to_be_visible()
        expect(page.get_by_role("gridcell", name="-").nth(1)).to_be_visible()

        #組み合わせ自動生成
        page.get_by_test_id("combination-gen").click()
        page.get_by_role("button", name="実行").click()
        expect(page.get_by_test_id("hot-decisionTable-1")).to_match_aria_snapshot("- rowgroup:\n  - row \"有効/無効 Checked Checked Checked Checked\":\n    - gridcell \"有効/無効\"\n    - gridcell \"Checked\":\n      - checkbox \"Checked\" [checked]\n    - gridcell \"Checked\":\n      - checkbox \"Checked\" [checked]\n    - gridcell \"Checked\":\n      - checkbox \"Checked\" [checked]\n    - gridcell \"Checked\":\n      - checkbox \"Checked\" [checked]\n  - row \"1 2 3 4 \":\n    - gridcell\n    - gridcell \"1\"\n    - gridcell \"2\"\n    - gridcell \"3\"\n    - gridcell \"4 \":\n      - button \"\"\n  - row \"条件  条件①  条件①ーC Y Y N N\":\n    - gridcell \"条件 \":\n      - button \"\"\n    - gridcell \"条件① \":\n      - button \"\"\n    - gridcell \"条件①ーC\"\n    - gridcell \"Y\"\n    - gridcell \"Y\"\n    - gridcell \"N\"\n    - gridcell \"N\"\n  - row \"N N Y Y\":\n    - gridcell\n    - gridcell \"N\"\n    - gridcell \"N\"\n    - gridcell \"Y\"\n    - gridcell \"Y\"\n  - row \"Y N Y N\":\n    - gridcell\n    - gridcell \"Y\"\n    - gridcell \"N\"\n    - gridcell \"Y\"\n    - gridcell \"N\"\n  - row \"動作  動作①  動作①ーC - - - -\":\n    - gridcell \"動作 \":\n      - button \"\"\n    - gridcell \"動作① \":\n      - button \"\"\n    - gridcell \"動作①ーC\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n  - row \"- - - -\":\n    - gridcell\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n  - row \"- - - -\":\n    - gridcell\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"\n    - gridcell \"-\"")

        #テストケース生成
        page.get_by_role("button", name="テストケースを生成").click()
        expect(page.get_by_test_id("hot-decisionTable-2").locator("div").filter(has_text="条件①動作1条件①ーC-2条件①ーCその他-3-4その他-").nth(1)).to_be_visible()

        #CSVダウンロード
        with page.expect_download() as download_info:
            page.get_by_role("button", name="CSVダウンロード").first.click()
        download = download_info.value
            #ダウンロードされたファイル名を取得
        downloaded_file_name = download.suggested_filename
            #ファイル名確認
        date_format_regex = r'\d{4}-\d{2}-\d{2}'
        expected_file_name_pattern = rf"Decision-table_{date_format_regex}\.csv"


        #自動保存確認（自動保存ON）
        page.get_by_role("row").filter(has_text=re.compile(r"^条件$")).get_by_role("gridcell").click()
        page.get_by_role("row").filter(has_text=re.compile(r"^条件$")).get_by_role("gridcell").dblclick()
        page.get_by_role("textbox").nth(2).dblclick()
        page.get_by_role("textbox").nth(2).fill("条件②")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()
        expect(page.get_by_test_id("hot-decisionTable-1")).to_contain_text("条件②")
            #１秒待機
        sleep(1)
            #一覧に戻って確認
        page.get_by_test_id("back").click()
        page.get_by_role("button", name="decision_table 変更した名前").click()
        expect(page.get_by_test_id("hot-decisionTable-1")).to_contain_text("条件②")


        #自動保存確認（自動保存OFF）
        page.get_by_role("checkbox", name="自動保存ON").uncheck()
        expect(page.get_by_role("checkbox", name="自動保存OFF")).not_to_be_checked()

        page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(8) > td:nth-child(2)").click()
        page.locator(".ht_clone_inline_start > .wtHolder > .wtHider > .wtSpreader > .htCore > tbody > tr:nth-child(8) > td:nth-child(2)").dblclick()
        page.get_by_role("textbox").nth(2).dblclick()
        page.get_by_role("textbox").nth(2).fill("動作②")
            #フォーカスアウト
        page.get_by_role("textbox").nth(2).press("Enter")
        page.get_by_text("デシジョンテーブル", exact=True).click()
            #一覧に戻って確認
        page.get_by_test_id("save").click()
        page.locator("div").filter(has_text="お知らせフィードバックを送信ヘルププロフィールと設定保存に成功しました保存に成功しました").get_by_role("button").nth(1).click()
        page.get_by_test_id("back").click()
        page.get_by_role("button", name="decision_table 変更した名前").click()
        expect(page.get_by_test_id("hot-decisionTable-1")).to_contain_text("動作②")

        #デシジョンテーブル削除
        page.get_by_role("checkbox", name="自動保存OFF").check()
        page.locator("div").filter(has_text=re.compile(r"^保存$")).get_by_role("button").nth(1).click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_text("削除").click()

        page.goto("https://gihoz.com/users/dl_auto_test_support/repositories/test_PoC/folders/626577c0-3a90-4777-9b2a-ac74619ab3e9")
        expect(page.locator("#test-model-case-table")).to_match_aria_snapshot("- textbox\n- table:\n  - rowgroup:\n    - row \"名前 種類 更新日時 更新者\":\n      - cell \"名前\"\n      - cell \"種類\"\n      - cell \"更新日時\"\n      - cell \"更新者\"\n  - rowgroup:\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Changed Decision Table デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Changed Decision Table\":\n        - button \"decision_table Changed Decision Table\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n    - row /decision_table Untitled Decision Table Testing デシジョンテーブルテスト \\d+-\\d+-\\d+ \\d+:\\d+ dl_auto_test_support/:\n      - cell \"decision_table Untitled Decision Table Testing\":\n        - button \"decision_table Untitled Decision Table Testing\":\n          - img \"decision_table\"\n      - cell \"デシジョンテーブルテスト\"\n      - cell /\\d+-\\d+-\\d+ \\d+:\\d+/\n      - cell \"dl_auto_test_support\"\n- separator\n- text: \"1ページあたりの表示件数:\"\n- combobox:\n  - text: /\\d+/\n  - textbox: /\\d+/\n- text: 1-4件/全4件中\n- navigation \"ページネーション\":\n  - list:\n    - listitem:\n      - button \"最初のページ\" [disabled]\n    - listitem:\n      - button \"前のページ\" [disabled]\n    - listitem:\n      - button \"次のページ\" [disabled]\n    - listitem:\n      - button \"最後のページ\" [disabled]")


        # ---------------------
        context.close()
        browser.close()

