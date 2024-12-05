export const CBR_Events = {
    CBR__CHAT__SAVED           : 'cbr::chat:saved'          ,
    CBR__CHAT__SAVE_ERROR      : 'cbr::chat:save-error'     ,

    CBR__FILE__CANCEL          : 'cbr::file:cancel'         ,
    CBR__FILE__CHANGED         : 'cbr::file:changed'        ,
    CBR__FILE__EDIT            : 'cbr::file:edit'           ,
    CBR__FILE__EDIT_MODE       : 'cbr::file:edit-mode'      ,
    CBR__FILE__GET_CONTENT     : 'cbr::file:get-content'    ,
    CBR__FILE__VIEW_MODE       : 'cbr::file:view-mode'      ,
    CBR__FILE__LOAD            : 'cbr::file:load'           ,
    CBR__FILE__LOAD_ERROR      : 'cbr::file:load-error'     ,
    CBR__FILE__LOADED          : 'cbr::file:loaded'         ,
    CBR__FILE__SAVED           : 'cbr::file:saved'          ,
    CBR__FILE__SAVE            : 'cbr::file:save'           ,
    CBR__FILE__SAVE_ERROR      : 'cbr::file:save-error'     ,
    CBR__FILE__SHOW_HISTORY    : 'cbr::file:show-history'   ,
    CBR__FILE__HIDE_HISTORY    : 'cbr::file:hide-history'   ,

    CBR__UI__LEFT_MENU_TOGGLE  : 'cbr::ui::left-menu:toggle' ,
    CBR__UI__NEW_ERROR_MESSAGE : 'cbr::ui::new-error-message',

    CBR__LLM__REQUEST__ERROR      : 'cbr::llm::request::error'   ,
    CBR__LLM__REQUEST__FINISHED   : 'cbr::llm::request::finished',
    CBR__LLM__REQUEST__STARTED    : 'cbr::llm::request::started' ,

    CBR__SESSION__PERSONA__CHANGED: 'cbr::user::persona::changed',

}

export default CBR_Events;