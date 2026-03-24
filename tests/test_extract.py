from utils.extract import scrape_page, extract_data
import requests

def test_scrape_page_success(mocker):
    mock_html = """
    <div class="product-details">
        <h3 class="product-title">T-shirt 1</h3>
        <div class="price-container"><span class="price">$10.00</span></div>
        <p>Rating: ⭐️ 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    mock_response = mocker.Mock()
    mock_response.content = mock_html
    mocker.patch('requests.get', return_value=mock_response)
    
    result = scrape_page("http://dummy.url")
    assert len(result) == 1
    assert result[0]['Title'] == "T-shirt 1"
    assert result[0]['Price'] == "$10.00"

def test_scrape_page_request_exception(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Mocked error"))
    result = scrape_page("http://dummy.url")
    assert result is None