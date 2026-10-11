from __future__ import annotations

import base64
import copy
import json
import mimetypes
import os
import re
import zipfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).parent
COMPONENT_DIR = APP_DIR / "visual_editor_component"
EXPORT_DIR = APP_DIR / "export"
CATEGORIES = [
    "現場風景",
    "壁紙貼り替え",
    "床工事",
    "店舗施工",
    "住宅施工",
    "女性監督の挨拶",
    "YouTubeショート",
    "PR動画",
]
VIEWPORTS = {
    "PC表示": 1180,
    "タブレット表示": 820,
    "スマホ表示": 390,
}


st.set_page_config(page_title="HP Visual Editor", page_icon="🎨", layout="wide")


visual_editor = components.declare_component("visual_editor", path=str(COMPONENT_DIR))


def uid(prefix: str) -> str:
    stamp = datetime.now().strftime("%H%M%S%f")
    return f"{prefix}-{stamp}"


def default_project() -> dict[str, Any]:
    now = datetime.now().strftime("%Y-%m-%d")
    return {
        "name": "HP Visual Editor Project",
        "pageTitle": "ネットインテリア月島",
        "background": "#f8f5ef",
        "viewport": "PC表示",
        "elements": [
            {
                "id": "logo-title",
                "type": "heading",
                "name": "メインコピー",
                "content": "ネットインテリア月島",
                "x": 80,
                "y": 48,
                "w": 520,
                "h": 70,
                "z": 2,
                "visible": True,
                "locked": False,
                "style": {
                    "fontSize": 42,
                    "fontWeight": 800,
                    "color": "#1f2933",
                    "background": "transparent",
                    "align": "left",
                    "radius": 0,
                    "border": 0,
                    "shadow": False,
                    "opacity": 1,
                    "lineHeight": 1.25,
                    "letterSpacing": 0,
                    "paddingY": 0,
                    "paddingX": 0,
                    "animation": "下から表示",
                },
                "responsive": {"mobile": {"x": 24, "y": 32, "w": 320, "h": 84, "fontSize": 30, "visible": True}},
            },
            {
                "id": "lead-text",
                "type": "text",
                "name": "説明文",
                "content": "壁紙・床・店舗内装の施工事例を、写真と動画でわかりやすく紹介します。",
                "x": 82,
                "y": 128,
                "w": 600,
                "h": 68,
                "z": 2,
                "visible": True,
                "locked": False,
                "style": {
                    "fontSize": 20,
                    "fontWeight": 500,
                    "color": "#4b5563",
                    "background": "transparent",
                    "align": "left",
                    "radius": 0,
                    "border": 0,
                    "shadow": False,
                    "opacity": 1,
                    "lineHeight": 1.55,
                    "letterSpacing": 0,
                    "paddingY": 0,
                    "paddingX": 0,
                    "animation": "なし",
                },
                "responsive": {"mobile": {"x": 24, "y": 124, "w": 320, "h": 96, "fontSize": 17, "visible": True}},
            },
            {
                "id": "hero-video",
                "type": "video",
                "name": "注目動画プレイヤー",
                "content": "ここに動画を追加",
                "src": "",
                "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "poster": "",
                "x": 80,
                "y": 230,
                "w": 760,
                "h": 430,
                "z": 1,
                "visible": True,
                "locked": False,
                "video": {
                    "autoplay": False,
                    "loop": False,
                    "muted": True,
                    "controls": True,
                    "playsinline": True,
                    "desktopOnly": False,
                    "mobileOnly": False,
                    "hideOnMobile": False,
                },
                "style": {
                    "fontSize": 18,
                    "fontWeight": 700,
                    "color": "#334155",
                    "background": "#111827",
                    "align": "center",
                    "radius": 18,
                    "border": 1,
                    "shadow": True,
                    "opacity": 1,
                    "lineHeight": 1.2,
                    "letterSpacing": 0,
                    "paddingY": 0,
                    "paddingX": 0,
                    "objectFit": "cover",
                    "animation": "フェードイン",
                },
                "responsive": {"mobile": {"x": 18, "y": 250, "w": 354, "h": 214, "visible": True}},
            },
            {
                "id": "contact-button",
                "type": "button",
                "name": "問い合わせボタン",
                "content": "問い合わせする",
                "href": "mailto:info@example.com",
                "x": 880,
                "y": 500,
                "w": 220,
                "h": 58,
                "z": 3,
                "visible": True,
                "locked": False,
                "style": {
                    "fontSize": 18,
                    "fontWeight": 800,
                    "color": "#ffffff",
                    "background": "#0f766e",
                    "align": "center",
                    "radius": 12,
                    "border": 0,
                    "shadow": True,
                    "opacity": 1,
                    "lineHeight": 1,
                    "letterSpacing": 0,
                    "paddingY": 0,
                    "paddingX": 0,
                    "animation": "なし",
                },
                "responsive": {"mobile": {"x": 72, "y": 486, "w": 246, "h": 56, "visible": True}},
            },
        ],
        "videos": [
            {
                "id": "sample-video",
                "title": "現場の風景",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "mp4": "",
                "github": "",
                "thumbnail": "",
                "description": "トップページに置ける注目動画のサンプルです。",
                "category": "現場風景",
                "date": now,
                "visible": True,
                "showTop": True,
                "showGallery": True,
                "order": 1,
            }
        ],
        "assets": [],
        "history": [],
        "future": [],
    }


def ensure_project() -> None:
    if "project" not in st.session_state:
        st.session_state.project = default_project()
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = st.session_state.project["elements"][0]["id"]


def find_element(project: dict[str, Any], element_id: str | None) -> dict[str, Any] | None:
    for element in project.get("elements", []):
        if element.get("id") == element_id:
            return element
    return None


def snapshot() -> None:
    project = st.session_state.project
    project.setdefault("history", []).append(copy.deepcopy({k: v for k, v in project.items() if k not in {"history", "future"}}))
    project["history"] = project["history"][-40:]
    project["future"] = []


def restore_state(state: dict[str, Any]) -> None:
    history = st.session_state.project.get("history", [])
    future = st.session_state.project.get("future", [])
    st.session_state.project = copy.deepcopy(state)
    st.session_state.project["history"] = history
    st.session_state.project["future"] = future


def add_element(kind: str, name: str) -> None:
    snapshot()
    base = {
        "id": uid(kind),
        "type": kind,
        "name": name,
        "content": {
            "image": "ここに画像を追加",
            "video": "ここに動画を追加",
            "text": "ここに文字を入力",
            "heading": "見出しを入力",
            "button": "ボタン",
            "divider": "",
            "spacer": "",
            "section": "セクション",
            "youtube": "YouTube動画",
            "gallery": "画像ギャラリー",
            "beforeafter": "Before / After",
            "slider": "スライダー",
            "video-list": "動画一覧",
        }.get(kind, name),
        "x": 90,
        "y": 90 + len(st.session_state.project["elements"]) * 20,
        "w": 320 if kind not in {"video", "youtube"} else 520,
        "h": 180 if kind not in {"text", "heading", "button", "divider", "spacer"} else 70,
        "z": len(st.session_state.project["elements"]) + 1,
        "visible": True,
        "locked": False,
        "style": {
            "fontSize": 18 if kind != "heading" else 32,
            "fontWeight": 700 if kind in {"heading", "button"} else 500,
            "color": "#111827",
            "background": "#ffffff" if kind not in {"text", "heading", "divider", "spacer"} else "transparent",
            "align": "center",
            "radius": 14,
            "border": 1 if kind not in {"text", "heading", "spacer"} else 0,
            "shadow": kind in {"image", "video", "youtube", "button"},
            "opacity": 1,
            "lineHeight": 1.35,
            "letterSpacing": 0,
            "paddingY": 10,
            "paddingX": 12,
            "objectFit": "cover",
            "animation": "なし",
        },
        "responsive": {"mobile": {"x": 24, "y": 80, "w": 340, "h": 180, "visible": True}},
    }
    if kind == "image":
        base["src"] = ""
    if kind in {"video", "youtube"}:
        base["src"] = ""
        base["youtube"] = ""
        base["poster"] = ""
        base["video"] = {"autoplay": False, "loop": False, "muted": True, "controls": True, "playsinline": True, "desktopOnly": False, "mobileOnly": False, "hideOnMobile": False}
    if kind == "button":
        base["href"] = "#"
        base["style"]["background"] = "#0f766e"
        base["style"]["color"] = "#ffffff"
    if kind == "divider":
        base["h"] = 8
        base["style"]["background"] = "#94a3b8"
    st.session_state.project["elements"].append(base)
    st.session_state.selected_id = base["id"]


def duplicate_element(element_id: str) -> None:
    element = find_element(st.session_state.project, element_id)
    if not element:
        return
    snapshot()
    clone = copy.deepcopy(element)
    clone["id"] = uid(element["type"])
    clone["name"] = f"{element.get('name', '要素')} コピー"
    clone["x"] = element.get("x", 0) + 24
    clone["y"] = element.get("y", 0) + 24
    clone["z"] = max([e.get("z", 0) for e in st.session_state.project["elements"]] + [0]) + 1
    st.session_state.project["elements"].append(clone)
    st.session_state.selected_id = clone["id"]


def delete_element(element_id: str) -> None:
    snapshot()
    st.session_state.project["elements"] = [e for e in st.session_state.project["elements"] if e["id"] != element_id]
    st.session_state.selected_id = st.session_state.project["elements"][0]["id"] if st.session_state.project["elements"] else None


def image_to_data_url(uploaded_file: Any) -> str:
    mime = uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(uploaded_file.getvalue()).decode('ascii')}"


def youtube_id(url: str) -> str:
    patterns = [
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url or "")
        if match:
            return match.group(1)
    return ""


def render_element_html(element: dict[str, Any], mobile: bool = False) -> str:
    item = copy.deepcopy(element)
    if mobile:
        overrides = item.get("responsive", {}).get("mobile", {})
        item.update({k: v for k, v in overrides.items() if k in {"x", "y", "w", "h", "visible"}})
        if "fontSize" in overrides:
            item.setdefault("style", {})["fontSize"] = overrides["fontSize"]
    if not item.get("visible", True):
        return ""
    style = item.get("style", {})
    css = (
        f"left:{item.get('x', 0)}px;top:{item.get('y', 0)}px;width:{item.get('w', 100)}px;height:{item.get('h', 50)}px;"
        f"z-index:{item.get('z', 1)};border-radius:{style.get('radius', 0)}px;opacity:{style.get('opacity', 1)};"
        f"color:{style.get('color', '#111')};background:{style.get('background', 'transparent')};"
        f"text-align:{style.get('align', 'left')};font-size:{style.get('fontSize', 16)}px;font-weight:{style.get('fontWeight', 500)};"
        f"line-height:{style.get('lineHeight', 1.35)};letter-spacing:{style.get('letterSpacing', 0)}px;"
        f"padding:{style.get('paddingY', 0)}px {style.get('paddingX', 0)}px;"
        f"border:{style.get('border', 0)}px solid #cbd5e1;"
        f"box-shadow:{'0 16px 36px rgba(15,23,42,.18)' if style.get('shadow') else 'none'};"
    )
    cls = f"el anim-{style.get('animation', 'なし')}"
    content = str(item.get("content", ""))
    if item["type"] == "image":
        src = item.get("src", "")
        inner = f"<img src='{src}' alt='{content}' style='width:100%;height:100%;object-fit:{style.get('objectFit','cover')};border-radius:inherit'>" if src else f"<div class='placeholder'>{content}</div>"
    elif item["type"] in {"video", "youtube"}:
        yt = youtube_id(item.get("youtube", ""))
        if yt:
            inner = f"<iframe src='https://www.youtube.com/embed/{yt}' title='{content}' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe>"
        elif item.get("src"):
            video = item.get("video", {})
            attrs = " controls" if video.get("controls", True) else ""
            attrs += " autoplay" if video.get("autoplay") else ""
            attrs += " loop" if video.get("loop") else ""
            attrs += " muted" if video.get("muted", True) else ""
            attrs += " playsinline" if video.get("playsinline", True) else ""
            poster = f" poster='{item.get('poster')}'" if item.get("poster") else ""
            inner = f"<video src='{item.get('src')}'{poster}{attrs}></video>"
        else:
            inner = f"<div class='placeholder video'>{content}</div>"
    elif item["type"] == "button":
        inner = f"<a href='{item.get('href', '#')}'>{content}</a>"
    elif item["type"] == "divider":
        inner = ""
    else:
        tag = "h1" if item["type"] == "heading" else "div"
        inner = f"<{tag}>{content}</{tag}>"
    return f"<div class='{cls}' style='{css}'>{inner}</div>"


def exported_files(project: dict[str, Any], mobile: bool = False) -> dict[str, bytes]:
    title = project.get("pageTitle", "HP Visual Editor")
    body = "\n".join(render_element_html(e, mobile=mobile) for e in sorted(project.get("elements", []), key=lambda x: x.get("z", 0)))
    videos = [v for v in project.get("videos", []) if v.get("visible") and v.get("showGallery")]
    gallery = "".join(
        f"<article class='video-card'><div class='thumb'>{('<img src='+json.dumps(v.get('thumbnail'))+'>' if v.get('thumbnail') else '▶')}</div>"
        f"<h3>{v.get('title','')}</h3><p>{v.get('description','')}</p><span>{v.get('category','')}</span></article>"
        for v in sorted(videos, key=lambda x: x.get("order", 0))
    )
    index = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="page">
{body}
  </main>
  <section class="video-gallery">
    <h2>動画ギャラリー</h2>
    <div class="video-grid">{gallery}</div>
  </section>
  <script src="script.js"></script>
</body>
</html>
"""
    css = f"""*{{box-sizing:border-box}}body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:{project.get('background','#fff')};color:#111827}}.page{{position:relative;min-height:780px;max-width:1180px;margin:0 auto;background:{project.get('background','#fff')}}}.el{{position:absolute;overflow:hidden}}.el iframe,.el video{{width:100%;height:100%;border:0;border-radius:inherit;object-fit:cover}}.el a{{display:flex;align-items:center;justify-content:center;width:100%;height:100%;color:inherit;text-decoration:none}}.placeholder{{display:flex;align-items:center;justify-content:center;width:100%;height:100%;border:2px dashed #94a3b8;border-radius:inherit;background:rgba(255,255,255,.75)}}.video-gallery{{max-width:1180px;margin:40px auto;padding:24px}}.video-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}}.video-card{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px;box-shadow:0 8px 20px rgba(15,23,42,.08)}}.thumb{{height:140px;border-radius:6px;background:#111827;color:white;display:flex;align-items:center;justify-content:center;font-size:34px;overflow:hidden}}.thumb img{{width:100%;height:100%;object-fit:cover}}.video-card h3{{margin:12px 0 6px;font-size:18px}}.video-card p{{margin:0 0 10px;color:#64748b}}.video-card span{{font-size:13px;color:#0f766e;font-weight:700}}@media(max-width:640px){{.page{{width:390px;max-width:100%;min-height:680px}}.video-gallery{{padding:18px}}}}"""
    js = """document.querySelectorAll('.anim-フェードイン,.anim-下から表示,.anim-上から表示,.anim-左から表示,.anim-右から表示,.anim-ズーム,.anim-スクロール時表示').forEach((el)=>{el.style.transition='opacity .55s ease, transform .55s ease';el.style.opacity='1';});"""
    return {
        "index.html": index.encode("utf-8"),
        "style.css": css.encode("utf-8"),
        "script.js": js.encode("utf-8"),
        "project.json": json.dumps(project, ensure_ascii=False, indent=2).encode("utf-8"),
    }


def zip_project(project: dict[str, Any]) -> bytes:
    files = exported_files(project)
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
        zf.writestr("assets/.gitkeep", "")
    return buffer.getvalue()


def save_export_to_disk(project: dict[str, Any]) -> None:
    EXPORT_DIR.mkdir(exist_ok=True)
    for name, data in exported_files(project).items():
        (EXPORT_DIR / name).write_bytes(data)
    (EXPORT_DIR / "assets").mkdir(exist_ok=True)


def github_push(project: dict[str, Any], owner: str, repo: str, branch: str) -> tuple[bool, str]:
    token = st.secrets.get("github", {}).get("token") or st.secrets.get("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        return False, "GitHubトークンが見つかりません。.streamlit/secrets.toml または Streamlit Cloud Secrets に設定してください。"
    files = exported_files(project)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    for path, content in files.items():
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        current = requests.get(url, headers=headers, params={"ref": branch}, timeout=20)
        payload: dict[str, Any] = {
            "message": f"Update {path} from HP Visual Editor",
            "content": base64.b64encode(content).decode("ascii"),
            "branch": branch,
        }
        if current.status_code == 200:
            payload["sha"] = current.json()["sha"]
        response = requests.put(url, headers=headers, json=payload, timeout=30)
        if response.status_code not in {200, 201}:
            return False, f"{path} の反映に失敗しました: {response.status_code} {response.text[:200]}"
    return True, "GitHubへ反映しました。"


def top_toolbar() -> None:
    project = st.session_state.project
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = st.columns([1, 1.3, 1, 1, 1, 1, 1, 1.2, 1.1, 1.4])
    if c1.button("新規ページ", use_container_width=True):
        st.session_state.project = default_project()
        st.session_state.selected_id = "logo-title"
        st.rerun()
    upload = c2.file_uploader("既存ページ / project.json", type=["json", "html"], label_visibility="collapsed")
    if upload:
        if upload.name.endswith(".json"):
            st.session_state.project = json.loads(upload.getvalue().decode("utf-8"))
            st.session_state.project.setdefault("history", [])
            st.session_state.project.setdefault("future", [])
            st.success("project.jsonを読み込みました。")
        else:
            html = upload.getvalue().decode("utf-8", errors="ignore")
            snapshot()
            st.session_state.project["elements"].append({
                "id": uid("html"),
                "type": "section",
                "name": "読み込んだHTML",
                "content": re.sub("<[^<]+?>", " ", html)[:300] or "読み込んだHTML",
                "x": 40,
                "y": 40,
                "w": 760,
                "h": 240,
                "z": 1,
                "visible": True,
                "locked": False,
                "style": {"fontSize": 16, "fontWeight": 500, "color": "#111827", "background": "#ffffff", "align": "left", "radius": 8, "border": 1, "shadow": False, "opacity": 1, "lineHeight": 1.5, "letterSpacing": 0, "paddingY": 16, "paddingX": 16, "animation": "なし"},
                "responsive": {"mobile": {"x": 16, "y": 40, "w": 356, "h": 260, "visible": True}},
            })
            st.info("HTMLを編集用セクションとして読み込みました。")
    for label, col in zip(VIEWPORTS.keys(), [c3, c4, c5]):
        if col.button(label, use_container_width=True):
            project["viewport"] = label
    if c6.button("元に戻す", use_container_width=True, disabled=not project.get("history")):
        current = copy.deepcopy({k: v for k, v in project.items() if k not in {"history", "future"}})
        previous = project["history"].pop()
        project.setdefault("future", []).append(current)
        restore_state(previous)
        st.rerun()
    if c7.button("やり直す", use_container_width=True, disabled=not project.get("future")):
        current = copy.deepcopy({k: v for k, v in project.items() if k not in {"history", "future"}})
        next_state = project["future"].pop()
        project.setdefault("history", []).append(current)
        restore_state(next_state)
        st.rerun()
    if c8.button("保存", use_container_width=True):
        save_export_to_disk(project)
        st.toast("export フォルダへ保存しました。")
    c9.download_button("HTML書き出し", exported_files(project)["index.html"], "index.html", "text/html", use_container_width=True)
    c10.download_button("ZIP書き出し", zip_project(project), "hp-visual-editor-export.zip", "application/zip", use_container_width=True)


def left_panel() -> None:
    st.markdown("### 追加")
    buttons = [
        ("画像を追加", "image", "画像"),
        ("動画を追加", "video", "動画"),
        ("文字を追加", "text", "文字"),
        ("見出しを追加", "heading", "見出し"),
        ("ボタンを追加", "button", "ボタン"),
        ("区切り線を追加", "divider", "区切り線"),
        ("背景を追加", "section", "背景"),
        ("空白を追加", "spacer", "空白"),
        ("セクションを追加", "section", "セクション"),
        ("画像ギャラリー", "gallery", "画像ギャラリー"),
        ("スライダー", "slider", "スライダー"),
        ("Before / After", "beforeafter", "Before / After"),
        ("YouTube", "youtube", "YouTube"),
        ("問い合わせボタン", "button", "問い合わせボタン"),
        ("動画一覧", "video-list", "動画一覧"),
    ]
    for i in range(0, len(buttons), 2):
        cols = st.columns(2)
        for col, item in zip(cols, buttons[i : i + 2]):
            if col.button(item[0], use_container_width=True):
                add_element(item[1], item[2])
                st.rerun()
    st.divider()
    st.markdown("### レイヤー")
    project = st.session_state.project
    for element in sorted(project.get("elements", []), key=lambda e: e.get("z", 0), reverse=True):
        cols = st.columns([0.18, 0.18, 0.44, 0.2])
        visible = cols[0].checkbox("表示", element.get("visible", True), key=f"vis-{element['id']}", label_visibility="collapsed")
        locked = cols[1].checkbox("固定", element.get("locked", False), key=f"lock-{element['id']}", label_visibility="collapsed")
        if visible != element.get("visible", True) or locked != element.get("locked", False):
            element["visible"] = visible
            element["locked"] = locked
        if cols[2].button(element.get("name", element["type"]), key=f"sel-{element['id']}", use_container_width=True):
            st.session_state.selected_id = element["id"]
        if cols[3].button("複製", key=f"dup-layer-{element['id']}", use_container_width=True):
            duplicate_element(element["id"])
            st.rerun()
    st.divider()
    st.markdown("### 動画ライブラリ")
    with st.expander("動画を登録", expanded=False):
        title = st.text_input("動画タイトル")
        url = st.text_input("動画URL / YouTube URL / MP4 URL")
        thumb = st.text_input("サムネイルURL")
        desc = st.text_area("説明", height=80)
        cat = st.selectbox("カテゴリ", CATEGORIES)
        show_top = st.checkbox("トップに表示", value=True)
        show_gallery = st.checkbox("動画ギャラリーに表示", value=True)
        uploaded_video = st.file_uploader("動画ファイルをアップロード", type=["mp4", "webm"], key="video-upload")
        if st.button("動画を登録", use_container_width=True):
            src = image_to_data_url(uploaded_video) if uploaded_video else url
            snapshot()
            st.session_state.project["videos"].append({
                "id": uid("video-lib"),
                "title": title or "無題の動画",
                "url": url,
                "youtube": url if "youtu" in url else "",
                "mp4": src if src and "youtu" not in src else "",
                "github": url if "github" in url else "",
                "thumbnail": thumb,
                "description": desc,
                "category": cat,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "visible": True,
                "showTop": show_top,
                "showGallery": show_gallery,
                "order": len(st.session_state.project["videos"]) + 1,
            })
            st.rerun()
    for video in sorted(project.get("videos", []), key=lambda v: v.get("order", 0)):
        with st.container(border=True):
            st.caption(video.get("category", ""))
            st.write(video.get("title", "無題"))
            if st.button("ページに追加", key=f"add-video-{video['id']}", use_container_width=True):
                add_element("video", video.get("title", "動画"))
                element = find_element(project, st.session_state.selected_id)
                if element:
                    element["youtube"] = video.get("youtube", "")
                    element["src"] = video.get("mp4") or video.get("url", "")
                    element["poster"] = video.get("thumbnail", "")
                    element["content"] = video.get("title", "動画")
                st.rerun()


def right_panel() -> None:
    project = st.session_state.project
    element = find_element(project, st.session_state.selected_id)
    st.markdown("### 設定")
    project["pageTitle"] = st.text_input("ページ名", project.get("pageTitle", ""))
    project["background"] = st.color_picker("背景色", project.get("background", "#ffffff"))
    if not element:
        st.info("中央の要素かレイヤーを選んでください。")
        return
    st.subheader(element.get("name", "選択中"))
    element["name"] = st.text_input("レイヤー名", element.get("name", ""), key=f"name-{element['id']}")
    if element["type"] in {"text", "heading", "button", "section", "gallery", "slider", "beforeafter", "video-list"}:
        element["content"] = st.text_area("文章", element.get("content", ""), height=90, key=f"content-{element['id']}")
    if element["type"] == "button":
        element["href"] = st.text_input("リンク先", element.get("href", "#"), key=f"href-{element['id']}")
    if element["type"] == "image":
        uploaded = st.file_uploader("画像を選択 / 差し替え", type=["jpg", "jpeg", "png", "webp"], key=f"image-{element['id']}")
        if uploaded:
            element["src"] = image_to_data_url(uploaded)
        element["src"] = st.text_input("画像URL", element.get("src", ""), key=f"src-{element['id']}")
        element["style"]["objectFit"] = st.selectbox("object-fit", ["cover", "contain", "fill"], index=["cover", "contain", "fill"].index(element["style"].get("objectFit", "cover")), key=f"fit-{element['id']}")
    if element["type"] in {"video", "youtube"}:
        uploaded_v = st.file_uploader("MP4 / WebMアップロード", type=["mp4", "webm"], key=f"mp4-{element['id']}")
        if uploaded_v:
            element["src"] = image_to_data_url(uploaded_v)
        element["src"] = st.text_input("動画URL / MP4 URL", element.get("src", ""), key=f"vsrc-{element['id']}")
        element["youtube"] = st.text_input("YouTube URL", element.get("youtube", ""), key=f"yt-{element['id']}")
        element["poster"] = st.text_input("poster画像", element.get("poster", ""), key=f"poster-{element['id']}")
        video = element.setdefault("video", {})
        cols = st.columns(2)
        video["autoplay"] = cols[0].checkbox("自動再生", video.get("autoplay", False), key=f"autoplay-{element['id']}")
        video["loop"] = cols[1].checkbox("ループ", video.get("loop", False), key=f"loop-{element['id']}")
        video["muted"] = cols[0].checkbox("ミュート", video.get("muted", True), key=f"muted-{element['id']}")
        video["controls"] = cols[1].checkbox("操作ボタン表示", video.get("controls", True), key=f"controls-{element['id']}")
        video["playsinline"] = cols[0].checkbox("playsinline", video.get("playsinline", True), key=f"plays-{element['id']}")
        video["desktopOnly"] = cols[1].checkbox("PCのみ表示", video.get("desktopOnly", False), key=f"pc-only-{element['id']}")
        video["mobileOnly"] = cols[0].checkbox("スマホのみ表示", video.get("mobileOnly", False), key=f"sp-only-{element['id']}")
        video["hideOnMobile"] = cols[1].checkbox("スマホでは非表示", video.get("hideOnMobile", False), key=f"hide-sp-{element['id']}")
    st.markdown("#### 位置とサイズ")
    c1, c2 = st.columns(2)
    element["x"] = c1.number_input("左", value=int(element.get("x", 0)), key=f"x-{element['id']}")
    element["y"] = c2.number_input("上", value=int(element.get("y", 0)), key=f"y-{element['id']}")
    element["w"] = c1.number_input("幅", min_value=10, value=int(element.get("w", 100)), key=f"w-{element['id']}")
    element["h"] = c2.number_input("高さ", min_value=4, value=int(element.get("h", 50)), key=f"h-{element['id']}")
    st.markdown("#### スマホ表示")
    mobile = element.setdefault("responsive", {}).setdefault("mobile", {})
    mobile["x"] = c1.number_input("スマホ 左", value=int(mobile.get("x", element.get("x", 0))), key=f"mx-{element['id']}")
    mobile["y"] = c2.number_input("スマホ 上", value=int(mobile.get("y", element.get("y", 0))), key=f"my-{element['id']}")
    mobile["w"] = c1.number_input("スマホ 幅", min_value=10, value=int(mobile.get("w", min(340, element.get("w", 100)))), key=f"mw-{element['id']}")
    mobile["h"] = c2.number_input("スマホ 高さ", min_value=4, value=int(mobile.get("h", element.get("h", 50))), key=f"mh-{element['id']}")
    mobile["fontSize"] = st.slider("スマホ文字サイズ", 8, 80, int(mobile.get("fontSize", element["style"].get("fontSize", 16))), key=f"mfs-{element['id']}")
    mobile["visible"] = st.checkbox("スマホで表示", mobile.get("visible", True), key=f"mvis-{element['id']}")
    st.markdown("#### 見た目")
    style = element.setdefault("style", {})
    style["fontSize"] = st.slider("文字サイズ", 8, 96, int(style.get("fontSize", 16)), key=f"fs-{element['id']}")
    style["fontWeight"] = st.select_slider("太さ", options=[300, 400, 500, 600, 700, 800, 900], value=int(style.get("fontWeight", 500)), key=f"fw-{element['id']}")
    style["color"] = st.color_picker("文字色", style.get("color", "#111827"), key=f"color-{element['id']}")
    style["background"] = st.text_input("背景色", style.get("background", "transparent"), key=f"bg-{element['id']}")
    style["align"] = st.segmented_control("文字揃え", ["left", "center", "right"], default=style.get("align", "left"), key=f"align-{element['id']}")
    style["lineHeight"] = st.slider("行間", 0.8, 2.5, float(style.get("lineHeight", 1.35)), 0.05, key=f"lh-{element['id']}")
    style["letterSpacing"] = st.slider("文字間隔", 0, 12, int(style.get("letterSpacing", 0)), key=f"ls-{element['id']}")
    style["paddingY"] = st.slider("上下余白", 0, 80, int(style.get("paddingY", 0)), key=f"py-{element['id']}")
    style["paddingX"] = st.slider("左右余白", 0, 80, int(style.get("paddingX", 0)), key=f"px-{element['id']}")
    style["radius"] = st.slider("角丸", 0, 80, int(style.get("radius", 0)), key=f"radius-{element['id']}")
    style["border"] = st.slider("枠線", 0, 12, int(style.get("border", 0)), key=f"border-{element['id']}")
    style["shadow"] = st.checkbox("影", bool(style.get("shadow", False)), key=f"shadow-{element['id']}")
    style["opacity"] = st.slider("透明度", 0.0, 1.0, float(style.get("opacity", 1)), 0.05, key=f"opacity-{element['id']}")
    style["animation"] = st.selectbox("アニメーション", ["なし", "フェードイン", "下から表示", "上から表示", "左から表示", "右から表示", "ズーム", "スクロール時表示"], index=["なし", "フェードイン", "下から表示", "上から表示", "左から表示", "右から表示", "ズーム", "スクロール時表示"].index(style.get("animation", "なし")), key=f"anim-{element['id']}")
    cdel, cdup = st.columns(2)
    if cdup.button("複製", use_container_width=True, key=f"dup-{element['id']}"):
        duplicate_element(element["id"])
        st.rerun()
    if cdel.button("削除", use_container_width=True, key=f"del-{element['id']}"):
        delete_element(element["id"])
        st.rerun()


def github_panel() -> None:
    with st.expander("GitHubへ反映", expanded=False):
        st.caption("トークンはソースコードに書かず、Streamlit Secrets の `GITHUB_TOKEN` または `[github] token` を使います。")
        owner = st.text_input("GitHubユーザー / 組織")
        repo = st.text_input("リポジトリ名", "hp-visual-editor")
        branch = st.text_input("ブランチ", "main")
        if st.button("GitHubへ反映", use_container_width=True):
            ok, message = github_push(st.session_state.project, owner, repo, branch)
            (st.success if ok else st.error)(message)


def main() -> None:
    ensure_project()
    st.markdown(
        """
        <style>
        .stApp { background: #eef2f1; }
        button[kind="secondary"], .stDownloadButton button { min-height: 42px; font-weight: 700; }
        section[data-testid="stSidebar"] { width: 360px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("HP Visual Editor")
    top_toolbar()
    project = st.session_state.project
    left, center, right = st.columns([0.24, 0.52, 0.24], gap="medium")
    with left:
        left_panel()
    with center:
        st.caption("中央の画面でクリック、ドラッグ、四隅リサイズ、文字の直接編集ができます。変更は自動で右側設定にも戻ります。")
        value = visual_editor(
            project=project,
            selectedId=st.session_state.selected_id,
            viewport=project.get("viewport", "PC表示"),
            width=VIEWPORTS.get(project.get("viewport", "PC表示"), 1180),
            key="visual-editor",
            default=None,
        )
        if value and isinstance(value, dict):
            if value.get("type") == "select":
                st.session_state.selected_id = value.get("id")
                st.rerun()
            if value.get("type") == "update":
                updated = value.get("project")
                if isinstance(updated, dict):
                    updated.setdefault("history", project.get("history", []))
                    updated.setdefault("future", project.get("future", []))
                    st.session_state.project = updated
                    st.session_state.selected_id = value.get("selectedId", st.session_state.selected_id)
                    st.rerun()
        github_panel()
        st.download_button("project.jsonをダウンロード", json.dumps(project, ensure_ascii=False, indent=2), "project.json", "application/json", use_container_width=True)
    with right:
        right_panel()


if __name__ == "__main__":
    main()
