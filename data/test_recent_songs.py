from generate_recent_songs import parseDiff, SongUpdate
patch = """
diff --git a/data/requirements.txt b/data/requirements.txt
index af0c4ae..f72571a 100644
--- a/data/requirements.txt
+++ b/data/requirements.txt
@@ -1,7 +1,18 @@
+async-timeout==4.0.3
+certifi==2024.7.4
+cffi==1.17.1
+charset-normalizer==3.3.2
 chevron==0.14.0
 exceptiongroup==1.2.2
+idna==3.7
 iniconfig==2.0.0
 packaging==24.1
 pluggy==1.5.0
+pycparser==2.22
+pygit2==1.15.1
 pytest==8.3.2
+redis==5.0.8
+requests==2.32.3
+spotipy==2.24.0
 tomli==2.0.1
+urllib3==2.2.2
diff --git a/dbexport.csv b/dbexport.csv
index bb4d22b..0059fe7 100644
--- a/dbexport.csv
+++ b/dbexport.csv
@@ -332,6 +332,7 @@
 "Killers, The","Mr. Brightside","c1X3Lg7RVkk","E:/Karaoke/Songs/Killers, The - Mr. Brightside - c1X3Lg7RVkk.mp4"
 "Killers, The","Somebody Told Me","p11rc6Qhuho","E:/Karaoke/Songs/Killers, The - Somebody Told Me - p11rc6Qhuho.mp4"
 "Kim Petras","There Will Be Blood","jkffV6VNfbA","E:/Karaoke/Songs/Kim Petras - There Will Be Blood - jkffV6VNfbA.mkv"
+"Korn","Another Brick in the Wall","3RFmrY Seks","E:/Karaoke/Songs/Korn - Another Brick in the Wall - 3RFmrY_Seks.mkv"
 "Lana Del Rey","Million Dollar Man","vQ2R 8iRfzU","E:/Karaoke/Songs/Lana Del Rey - Million Dollar Man - vQ2R_8iRfzU.mp4"
 "Laufey","From the Start","3vCD1mQlDlg","E:/Karaoke/Songs/Laufey - From the Start - 3vCD1mQlDlg.mp4"
 "Laura Branigan","Gloria","y4gtIRSt1Z4","E:/Karaoke/Songs/Laura Branigan - Gloria - y4gtIRSt1Z4.mp4"
@@ -581,7 +582,6 @@
 "Smiths, The","There Is a Light That Never Goes Out","jkULDIk23KU","E:/Karaoke/Songs/Smiths, The - There Is a Light That Never Goes Out - jkULDIk23KU.mp4"
 "Soft Cell","Tainted Love","WGbHRHRYo20","E:/Karaoke/Songs/Soft Cell - Tainted Love - WGbHRHRYo20.mp4"
 "Sonic Adventure","Believe in Myself (Tails' Theme)","JDlQARZS31Y","E:/Karaoke/Songs/Sonic Adventure - Believe in Myself (Tails' Theme) - JDlQARZS31Y.mkv"
-"Sonic Adventure","Escape from the City","5bjULQizgfw","E:/Karaoke/Songs/Sonic Adventure - Escape from the City - 5bjULQizgfw.mp4"
 "Sonic Adventure","It Doesn't Matter (Sonic's Theme)","G2nte pmPQE","E:/Karaoke/Songs/Sonic Adventure - It Doesn't Matter (Sonic's Theme) - G2nte_pmPQE.mkv"
 "Sonic Adventure","Lazy Days (Duet) (Big's Theme)","eYHWFFGHilI","E:/Karaoke/Songs/Sonic Adventure - Lazy Days (Duet) (Big's Theme) - eYHWFFGHilI.mkv"
 "Sonic Adventure","My Sweet Passion (Amy's Theme)","V27E3gYrnXQ","E:/Karaoke/Songs/Sonic Adventure - My Sweet Passion (Amy's Theme) - V27E3gYrnXQ.mkv"
@@ -589,6 +589,7 @@
 "Sonic Adventure","Unknown from M.E. (Knuckles' Theme)","16P-TFAEutU","E:/Karaoke/Songs/Sonic Adventure - Unknown from M.E. (Knuckles' Theme) - 16P-TFAEutU.mkv"
 "Sonic Adventure 2","Believe in Myself (Tails' Theme)","rM5gnVG8DbQ","E:/Karaoke/Songs/Sonic Adventure 2 - Believe in Myself (Tails' Theme) - rM5gnVG8DbQ.mkv"
 "Sonic Adventure 2","E.G.G.M.A.N. (Eggman's Theme)","7AJX9N0ZzaY","E:/Karaoke/Songs/Sonic Adventure 2 - E.G.G.M.A.N. (Eggman's Theme) - 7AJX9N0ZzaY.mkv"
+"Sonic Adventure 2","Escape from the City","5bjULQizgfw","E:/Karaoke/Songs/Sonic Adventure 2 - Escape from the City - 5bjULQizgfw.mp4"
 "Sonic Adventure 2","Fly in the Freedom (Rouge's Theme)","XmUB3KG RIQ","E:/Karaoke/Songs/Sonic Adventure 2 - Fly in the Freedom (Rouge's Theme) - XmUB3KG_RIQ.mkv"
 "Sonic Adventure 2","It Doesn't Matter (Sonic's Theme)","hUcir7t MIs","E:/Karaoke/Songs/Sonic Adventure 2 - It Doesn't Matter (Sonic's Theme) - hUcir7t_MIs.mkv"
 "Sonic Adventure 2","Live & Learn (Main Theme)","ozaYTjYygzc","E:/Karaoke/Songs/Sonic Adventure 2 - Live & Learn (Main Theme) - ozaYTjYygzc.mkv"
 """

def test():
    results = parseDiff(patch, 1741392817)
    assert list(results.keys()) == [
        "+2025-03-07 16:13:37KornAnother Brick in the Wall",
        "-2025-03-07 16:13:37Sonic AdventureEscape from the City",
        "+2025-03-07 16:13:37Sonic Adventure 2Escape from the City"
    ]
    
    assert len(results) == 3

    # assert results.values
    # {
    #     "+2025-03-07 16:13:37KornAnother Brick in the Wall": SongUpdate("+", "2025-03-07 16:13:37", "Korn", "Another Brick in the Wall"),
    #     "-2025-03-07 16:13:37Sonic AdventureEscape from the City": SongUpdate("-", "2025-03-07 16:13:37", "Sonic Adventure", "Escape from the City"),
    #     "+2025-03-07 16:13:37Sonic Adventure 2Escape from the City": SongUpdate("+", "2025-03-07 16:13:37", "Sonic Adventure 2", "Escape from the City"),
    # }