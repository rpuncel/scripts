from scripts.cal import Event, to_front_matter

def test_to_front_matter_with_times():
    event = Event(title="Test Event", date="2022-01-01", start_time="10:00", end_time="12:00")
    expected_output = "---\ntitle: Test Event\ndate: 2022-01-01\nstartTme: 10:00\nendTime: 12:00\nallDay: false\n---"
    assert to_front_matter(event) == expected_output

def test_to_front_matter_without_times():
    event = Event(title="Test Event", date="2022-01-01")
    expected_output = "---\ntitle: Test Event\ndate: 2022-01-01\nallDay: true\n---"
    assert to_front_matter(event) == expected_output

def test_file_creation(tmp_path):
    # Create a file inside the temporary directory
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Hello, world!")