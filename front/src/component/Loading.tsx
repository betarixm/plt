import React from 'react';

interface LoadingProps {
    description: string
}

interface LoadingStates {

}

class Loading extends React.Component<LoadingProps, LoadingStates> {
    render() {
        return (
            <div>
                {this.props.description}
            </div>
        )
    }
}

export default Loading;