from datetime import date, datetime, time, timedelta
from uuid import uuid4

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Aklımda",
    page_icon="🧠",
)


# -----------------------------------------------------------------------------
# Utilities

def init_state():
    if "reminders" in st.session_state:
        return

    today = date.today()
    st.session_state.reminders = [
        {
            "id": str(uuid4()),
            "title": "KPSS deneme sınavı",
            "category": "KPSS",
            "date": today + timedelta(days=1),
            "time": time(10, 0),
            "notes": "Sonuçları not et",
            "done": False,
        },
        {
            "id": str(uuid4()),
            "title": "İlaç iç - sabah dozu",
            "category": "İlaç",
            "date": today,
            "time": time(8, 30),
            "notes": "Kahvaltıdan sonra",
            "done": False,
        },
        {
            "id": str(uuid4()),
            "title": "YKS geometri tekrar",
            "category": "YKS",
            "date": today + timedelta(days=3),
            "time": time(19, 0),
            "notes": "Konu: çember ve daire",
            "done": False,
        },
        {
            "id": str(uuid4()),
            "title": "Haftalık toplantı",
            "category": "Toplantı",
            "date": today + timedelta(days=2),
            "time": time(14, 0),
            "notes": "Sunum dosyasını hazırla",
            "done": False,
        },
    ]


def add_reminder(title: str, category: str, date_value: date, time_value: time, notes: str):
    st.session_state.reminders.append(
        {
            "id": str(uuid4()),
            "title": title.strip(),
            "category": category,
            "date": date_value,
            "time": time_value,
            "notes": notes.strip(),
            "done": False,
        }
    )


def toggle_completion(reminder_id: str, done: bool):
    for reminder in st.session_state.reminders:
        if reminder["id"] == reminder_id:
            reminder["done"] = done
            break


def build_dataframe(reminders):
    df = pd.DataFrame(reminders)
    if df.empty:
        return df

    df["datetime"] = df.apply(
        lambda row: datetime.combine(row["date"], row["time"]), axis=1
    )
    df["Durum"] = df["done"].map({True: "Tamamlandı", False: "Aktif"})
    df = df.sort_values(["done", "datetime"])
    df["Tarih"] = df["datetime"].dt.strftime("%d %B %Y")
    df["Saat"] = df["datetime"].dt.strftime("%H:%M")
    df = df[
        [
            "title",
            "category",
            "Tarih",
            "Saat",
            "notes",
            "Durum",
            "id",
            "done",
        ]
    ].rename(
        columns={
            "title": "Başlık",
            "category": "Kategori",
            "notes": "Notlar",
        }
    )
    return df


# -----------------------------------------------------------------------------
# Page content

init_state()

st.title("🧠 Aklımda")
st.caption(
    "KPSS, YKS veya ilaç takibi gibi günlük işlerin unutulmaması için pratik hatırlatıcı."
)

st.divider()

col1, col2, col3 = st.columns(3)

reminders_df = build_dataframe(st.session_state.reminders)
aktif_sayisi = 0 if reminders_df.empty else reminders_df["Durum"].eq("Aktif").sum()

today = date.today()
today_tasks = 0
if not reminders_df.empty:
    today_tasks = reminders_df[
        (reminders_df["Tarih"] == today.strftime("%d %B %Y"))
        & (reminders_df["Durum"] == "Aktif")
    ].shape[0]

total = len(st.session_state.reminders)

col1.metric("Toplam Hatırlatıcı", total)
col2.metric("Aktif Görev", aktif_sayisi)
col3.metric("Bugün", today_tasks)

st.divider()

add_tab, list_tab = st.tabs(["Yeni hatırlatıcı ekle", "Planlarım"])

with add_tab:
    st.subheader("Yeni hatırlatıcı oluştur")
    with st.form("new_reminder"):
        title = st.text_input("Başlık", placeholder="Örn. KPSS deneme çöz")
        category = st.selectbox(
            "Kategori",
            ["KPSS", "YKS", "İlaç", "İş", "Toplantı", "Özel"],
        )
        col_left, col_right = st.columns(2)
        with col_left:
            reminder_date = st.date_input("Tarih", value=date.today())
        with col_right:
            reminder_time = st.time_input("Saat", value=time(9, 0))
        notes = st.text_area("Notlar", placeholder="Ek not bırakabilirsiniz")

        submitted = st.form_submit_button("Hatırlatıcıyı kaydet")

        if submitted:
            if not title.strip():
                st.warning("Başlık boş olamaz")
            else:
                add_reminder(title, category, reminder_date, reminder_time, notes)
                st.success("Hatırlatıcı eklendi")

with list_tab:
    st.subheader("Tüm hatırlatıcılar")
    if reminders_df.empty:
        st.info("Henüz hatırlatıcı yok. Yukarıdan bir tane ekleyin!")
    else:
        search = st.text_input("Başlıkta ara", placeholder="YKS deneme...", key="search")
        chosen_categories = st.multiselect(
            "Kategori filtrele",
            options=sorted(reminders_df["Kategori"].unique()),
            default=list(sorted(reminders_df["Kategori"].unique())),
        )
        status_filter = st.radio(
            "Durum",
            options=["Hepsi", "Aktif", "Tamamlandı"],
            horizontal=True,
        )

        filtered = reminders_df.copy()
        if search:
            filtered = filtered[filtered["Başlık"].str.contains(search, case=False, na=False)]
        if chosen_categories:
            filtered = filtered[filtered["Kategori"].isin(chosen_categories)]
        if status_filter != "Hepsi":
            filtered = filtered[filtered["Durum"] == status_filter]

        st.markdown("### Liste")
        if filtered.empty:
            st.info("Filtrelere uyan hatırlatıcı bulunamadı")
        else:
            for _, row in filtered.iterrows():
                container = st.container(border=True)
                col_a, col_b = container.columns([3, 1])
                with col_a:
                    st.write(f"**{row['Başlık']}** · {row['Kategori']}")
                    st.caption(f"{row['Tarih']} · {row['Saat']}")
                    if row["Notlar"]:
                        st.write(row["Notlar"])
                with col_b:
                    done = row["Durum"] == "Tamamlandı"
                    checked = st.checkbox("Tamamlandı", value=done, key=row["id"])
                    if checked != done:
                        toggle_completion(row["id"], checked)
                        st.rerun()

        st.divider()
        st.markdown("### Tablo görünümü")
        st.dataframe(
            filtered[["Başlık", "Kategori", "Tarih", "Saat", "Notlar", "Durum"]],
            use_container_width=True,
            hide_index=True,
        )
