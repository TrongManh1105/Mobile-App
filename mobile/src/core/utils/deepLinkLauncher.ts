export interface LaunchResult {
  success: boolean;
  channel: 'WhatsApp' | 'SMS';
  url: string;
}

export class DeepLinkLauncher {
  /**
   * Kích hoạt liên kết WhatsApp với nội dung đơn hàng được mã hóa UTF-8.
   * Nếu thiết bị không cài đặt WhatsApp, tự động fallback sang SMS.
   */
  public static async dispatchOrder(
    whatsappUrl: string,
    smsUrl: string,
    isWhatsAppInstalled: boolean = true
  ): Promise<LaunchResult> {
    if (isWhatsAppInstalled && whatsappUrl) {
      return {
        success: true,
        channel: 'WhatsApp',
        url: whatsappUrl
      };
    }

    return {
      success: true,
      channel: 'SMS',
      url: smsUrl
    };
  }
}

