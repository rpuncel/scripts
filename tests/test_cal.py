from scripts.cal import Event, Store, to_front_matter
import filecmp

def test_file_creation(datadir):
    # Create a file inside the temporary directory

    store = Store(datadir / 'actual')
    events = [
       Event(title="Test Event", date="2022-01-01", start_time="11:00", end_time="12:00"),
       Event(title="All Day Test Event", date="2022-01-02"),
       Event(title="Existing Test Event", date="2022-01-03", start_time="12:00", end_time="13:00")
    ] 
    for event in events:
        store.upsert_event(event)
    dircmp = filecmp.dircmp(datadir / 'actual', datadir / 'expects')
    assert len(dircmp.diff_files) == 0, "did not produce the expected set of files"
